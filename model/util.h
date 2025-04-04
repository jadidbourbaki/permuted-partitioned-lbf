#ifndef UTIL_H
#define UTIL_H

#include "model.h"

// varies alpha and generates a plot based on it. increment is the number to
// increment alpha with. p_weight is the probability with which
// the adversary chooses the query to be a false positive
void vary_alpha(const char *file, const double increment, struct model_state *s,
                const double p_weight);

// varies Q_{N} from 0 to 1 and generates a plot based on it.
void vary_q_n(const char *file, const double increment, struct model_state *s);

// varies the partition between false positives and false negatives from 0 to 1
// and generates a plot based on it.
void vary_p_weight(const char *file, const double increment,
                   struct model_state *s, const double alpha);

#endif // UTIL_H
