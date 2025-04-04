#include "util.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// varies alpha and generates a plot based on it. increment is the number to
// increment alpha with. p_weight is the probability with which
// the adversary chooses the query to be a false positive
void vary_alpha(const char *file, const double increment, struct model_state *s,
                const double p_weight) {
  assert(increment > 0 && increment < 1);
  size_t plot_size = (size_t)ceil(1 / increment) + 1;

  // should check for multiplication overflow here
  double *db_arr = malloc(sizeof(double) * plot_size);
  assert(db_arr != NULL);

  double *alpha_arr = malloc(sizeof(double) * plot_size);
  assert(alpha_arr != NULL);

  double classical =
      model_fpr_classical(s->n, model_total_memory_from_state(s), s->lambda);

  double alpha = 0.0;
  register size_t i;

  for (i = 0; i < plot_size; i++) {
    alpha_arr[i] = alpha;
    s->alpha_p = alpha * p_weight;
    s->alpha_n = alpha * (1 - p_weight);

    db_arr[i] = model_fpr_downtown_bodega_hybrid_from_state(s);
    alpha += increment;
  }

  // -- storing the data --
  FILE *data;

  data = fopen(file, "w");
  assert(data != NULL);

  fprintf(data, "alpha,downtown_fpr,classical_fpr\n");

  for (i = 0; i < plot_size; i++) {
    fprintf(data, "%f,%f,%f\n", alpha_arr[i], db_arr[i], classical);
  }

  fclose(data);

  free(alpha_arr);
  free(db_arr);
}

// varies Q_{N} from 0 to 1 and generates a plot based on it.
void vary_q_n(const char *file, const double increment, struct model_state *s) {
  assert(increment > 0 && increment < 1);
  size_t plot_size = (size_t)ceil(1 / increment) + 1;

  // should check for multiplication overflow here
  double *db_arr = malloc(sizeof(double) * plot_size);
  assert(db_arr != NULL);

  double *q_n_arr = malloc(sizeof(double) * plot_size);
  assert(q_n_arr != NULL);

  double classical =
      model_fpr_classical(s->n, model_total_memory_from_state(s), s->lambda);

  double q_n = 0.0;
  register size_t i;

  for (i = 0; i < plot_size; i++) {
    q_n_arr[i] = q_n;
    s->q = q_n;

    db_arr[i] = model_fpr_downtown_bodega_hybrid_from_state(s);
    q_n += increment;
  }

  // -- storing the data --
  FILE *data;

  data = fopen(file, "w");
  assert(data != NULL);

  fprintf(data, "q_n,downtown_fpr,classical_fpr\n");

  for (i = 0; i < plot_size; i++) {
    fprintf(data, "%f,%f,%f\n", q_n_arr[i], db_arr[i], classical);
  }

  fclose(data);

  free(q_n_arr);
  free(db_arr);
}

// varies the partition between false positives and false negatives from 0 to 1
// and generates a plot based on it.
void vary_p_weight(const char *file, const double increment,
                   struct model_state *s, const double alpha) {
  assert(increment > 0 && increment < 1);
  size_t plot_size = (size_t)ceil(1 / increment) + 1;

  // should check for multiplication overflow here
  double *db_arr = malloc(sizeof(double) * plot_size);
  assert(db_arr != NULL);

  double *p_weight_arr = malloc(sizeof(double) * plot_size);
  assert(p_weight_arr != NULL);

  double classical =
      model_fpr_classical(s->n, model_total_memory_from_state(s), s->lambda);

  double p_weight = 0.0;
  register size_t i;

  for (i = 0; i < plot_size; i++) {
    p_weight_arr[i] = p_weight;
    s->alpha_p = alpha * p_weight;
    s->alpha_n = alpha * (1 - p_weight);

    db_arr[i] = model_fpr_downtown_bodega_hybrid_from_state(s);
    p_weight += increment;
  }

  // -- storing the data --
  FILE *data;

  data = fopen(file, "w");
  assert(data != NULL);

  fprintf(data, "p_weight,downtown_fpr,classical_fpr\n");

  for (i = 0; i < plot_size; i++) {
    fprintf(data, "%f,%f,%f\n", p_weight_arr[i], db_arr[i], classical);
  }

  fclose(data);

  free(p_weight_arr);
  free(db_arr);
}
