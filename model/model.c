#include "model.h"

#include <assert.h>
#include <math.h>

// model_fpr_classical returns the False Positive Rate of a Secure Classical
// Bloom Filter. n is the cardinality of the set being encoded. m is the memory
// budget. lambda is the security parameter, in bit.
double model_fpr_classical(const uint64_t n, const uint64_t m,
                           const uint64_t lambda) {
  double reduced_m = m - lambda;
  // optimal number of hash functions
  double k = ceil(log(2) * (n / reduced_m));
  return pow(1.0 - exp(-1 * k * (n / reduced_m)), k);
}

// model_fpr_learned returns the False Positive Rate of a Bloom Filter Learning
// Model. n is the cardinality of the set being encoded. m is the memory budget.
// c is the ratio of the FPR of a Bloom Filter Learning Model and the FPR of a
// Classical Bloom Filter.
double model_fpr_learned(const uint64_t n, const uint64_t m, const double c) {
  return c * model_fpr_classical(n, m, 0);
}

// model_fnr_learned returned the False Negative Rate of a Bloom Filter Learning
// Model. Recall that a Bloom Filter Learning Model has a two-sided error, not a
// one-sided error like the Bloom Filter. In this model, we are assuming the
// false negative rate is the same as the false positive rate (i.e the
// probability of erring on either side is equal). This may be modified to test
// other scenarios.
#define model_fnr_learned(n, m, c) (model_fpr_learned(n, m, c))

// model_tnr_learned returns the True Negative Rate of a Bloom Filter Learning
// Model. n is the cardinality of the set being encoded. m is the memory budget.
// c is the ratio of the FPR of a Bloom Filter Learning Model and the FPR of a
// Classical Bloom Filter. q_n is the fraction of true negative non-adversarial
// queries.
double model_tnr_learned(const uint64_t n, const uint64_t m, const double c,
                         const double q_n) {
  return (1 - model_fpr_learned(n, m, c)) * q_n;
}

// n_backup_a returns the cardinality of the set being encoded by Backup Bloom
// Filter A
static uint64_t n_backup_a(const uint64_t n, const double m_l, const double c) {
  double fnr_l = model_fnr_learned(n, m_l, c);

  // The cardinality of the set being encoded by Backup Classical Bloom Filter
  // A. Recall that Backup Bloom Filter A only encodes the elements in the
  // original set marked positive by the Bloom Filter Learning Model. For a
  // Bloom Filter Learning Model with a False Negative Rate of 0, these will be
  // *all* the elements. For Bloom Filter Learning Model with a False Negative
  // Rate of 0.5, these will be half the elements. We round upwards, instead of
  // towards zero.
  uint64_t n_a = ceil(n * (1 - fnr_l));
  return n_a;
}

// n_backup_b returns the cardinality of the set being encoded by Backup Bloom
// Filter B
static uint64_t n_backup_b(const uint64_t n, const double m_l, const double c) {
  double fnr_l = model_fnr_learned(n, m_l, c);
  // Similar logic as `n_backup_a` applies to the cardinality of the set being
  // encoded by Backup Classical Bloom Filter B, which only encodes the elements
  // in the original set marked negative by the Bloom Filter Learning Model.
  uint64_t n_b = ceil(n * fnr_l);
  return n_b;
}

// model_fpr_downtown_bodega returns the False Positive Rate for the Downtown
// Bodega Filter. For more details, take a look at the "Hybrid Model" section in
// our paper. `n` is the cardinality of the set being encoded. `c` is the ratio
// of the False Positive Rate of the Bloom Filter Learning Model compared to the
// False Positive Rate of the Classical Bloom Filter with the same cardinality
// and memory budget. `q` is the fraction of true negative non-adversarial
// queries. `m_l`, `m_a`, and `m_b` is the memory budget (in bits) of the Bloom
// Filter Learning Model, the Backup Classical Bloom Filter A, and the Backup
// Classical Bloom Filter B respectively. `lambda` is the security parameter, in
// bits.
double model_fpr_downtown_bodega(const uint64_t n, const double c,
                                 const double q, const double m_l,
                                 const double m_a, const double m_b,
                                 const uint64_t lambda) {

  uint64_t n_a = n_backup_a(n, m_l, c);
  uint64_t n_b = n_backup_b(n, m_l, c);

  double fpr_l = model_fpr_learned(n, m_l, c);
  double fpr_a = model_fpr_classical(n_a, m_a, lambda);
  double tnr_l = model_tnr_learned(n, m_l, c, q);
  double fpr_b = model_fpr_classical(n_b, m_b, lambda);

  return fpr_l * fpr_a + tnr_l * fpr_b;
}

// model_fpr_downtown_bodega_hybrid returns the expected False Positive Rate of
// the Downtown Bodega Filter in the Hybrid Model.
// alpha = alpha_p + alpha_n is the fraction of queries chosen by an adversary.
// alpha_p are the queries that generate false positives in the Bloom Filter
// Learning Model alpha_n are the queries that generate true negatives in the
// Bloom Filter Learning Model `n` is the cardinality of the set being encoded.
// `c` is the ratio of the False Positive Rate of the Bloom Filter Learning
// Model compared to the False Positive Rate of the Classical Bloom Filter with
// the same cardinality and memory budget. `q` is the fraction of true negative
// non-adversarial queries. `m_l`, `m_a`, and `m_b` is the memory budget (in
// bits) of the Bloom Filter Learning Model, the Backup Classical Bloom Filter
// A, and the Backup Classical Bloom Filter B respectively. `lambda` is the
// security parameter, in bits.
double model_fpr_downtown_bodega_hybrid(const double alpha_p,
                                        const double alpha_n, const uint64_t n,
                                        const double c, const double q,
                                        const double m_l, const double m_a,
                                        const double m_b,
                                        const uint64_t lambda) {
  uint64_t n_a = n_backup_a(n, m_l, c);
  uint64_t n_b = n_backup_b(n, m_l, c);

  double fpr_a = model_fpr_classical(n_a, m_a, lambda);
  double fpr_b = model_fpr_classical(n_b, m_b, lambda);
  double fpr_db = model_fpr_downtown_bodega(n, c, q, m_l, m_a, m_b, lambda);

  return alpha_p * fpr_a + alpha_n * fpr_b + (1 - alpha_p - alpha_n) * fpr_db;
}

// model_total_memory_from_state returns the total memory budget available for
// the experiment.
double model_total_memory_from_state(const struct model_state *s) {
  return s->m_l + s->m_a + s->m_b;
}

// Similar to model_fpr_downtown_bodega_hybrid, but extracts information from
// the model state.
double
model_fpr_downtown_bodega_hybrid_from_state(const struct model_state *s) {
  return model_fpr_downtown_bodega_hybrid(s->alpha_p, s->alpha_n, s->n, s->c,
                                          s->q, s->m_l, s->m_a, s->m_b,
                                          s->lambda);
}
