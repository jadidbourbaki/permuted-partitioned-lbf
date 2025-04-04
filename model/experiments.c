#include "datasets.h"
#include "model.h"
#include "util.h"
#include <math.h>
#include <stdio.h>

int main(void) {
  struct model_state s;
  transparency_report(&s);
  vary_alpha("experiment_1_google_transparency.csv", 0.1, &s, 0.5);

  malicious_urls(&s);
  vary_alpha("experiment_1_malicious_urls.csv", 0.1, &s, 0.5);

  ember(&s);
  vary_alpha("experiment_1_ember.csv", 0.1, &s, 0.5);

  // back to transparency report
  transparency_report(&s);
  s.alpha_p = s.alpha_n = 0.1;

  vary_q_n("experiment_2_google_transparency_alpha_0p2.csv", 0.1, &s);

  s.alpha_p = s.alpha_n = 0.15;

  vary_q_n("experiment_2_google_transparency_alpha_0p3.csv", 0.1, &s);

  s.alpha_p = s.alpha_n = 0.25;

  vary_q_n("experiment_2_google_transparency_alpha_0p5.csv", 0.1, &s);

  s.alpha_p = s.alpha_n = 0.5;

  vary_q_n("experiment_2_google_transparency_alpha_1p0.csv", 0.1, &s);

  s.q = 0.5;

  vary_p_weight("experiment_3_google_transparency_alpha_0p2.csv", 0.1, &s, 0.2);

  return EXIT_SUCCESS;
}
