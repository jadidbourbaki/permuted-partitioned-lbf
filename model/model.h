#ifndef MODEL_H
#define MODEL_H

#include <stdlib.h>

// model_fpr_classical returns the False Positive Rate of a Secure Classical
// Bloom Filter. n is the cardinality of the set being encoded. m is the memory
// budget. lambda is the security parameter, in bit.
double model_fpr_classical(const uint64_t n, const uint64_t m,
                           const uint64_t lambda);

// model_fpr_learned returns the False Positive Rate of a Bloom Filter Learning
// Model. n is the cardinality of the set being encoded. m is the memory budget.
// c is the ratio of the FPR of a Bloom Filter Learning Model and the FPR of a
// Classical Bloom Filter.
double model_fpr_learned(const uint64_t n, const uint64_t m, const double c);

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
                         const double q_n);

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
                                 const uint64_t lambda);

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
                                        const uint64_t lambda);

// model_state contains all the information you need to run the model. Vary the
// following to see different results of the model.
struct model_state {
  // the ratio of the FPR of a Bloom Filter Learning Model to a
  // classical bloom filter
  double c;
  // the cardinality of the complete set
  uint64_t n;
  // the security parameter
  uint64_t lambda;
  // memory budget for the Bloom Filter Learning Model
  double m_l;
  // memory budget for Backup Classical Bloom Filter A
  double m_a;
  // memory budget for Backup Classical Bloom Filter B
  double m_b;
  // the fraction of true negative non-adversarial queries.
  double q;
  // fraction of false positive queries chosen by the adversary
  double alpha_p;
  // fraction of true negative queries chosen by the adversary
  double alpha_n;
};

// model_total_memory_from_state returns the total memory budget available for
// the experiment.
double model_total_memory_from_state(const struct model_state *s);

// Similar to model_fpr_downtown_bodega_hybrid, but extracts information from
// the model state.
double model_fpr_downtown_bodega_hybrid_from_state(const struct model_state *s);

#endif // MODEL_H
