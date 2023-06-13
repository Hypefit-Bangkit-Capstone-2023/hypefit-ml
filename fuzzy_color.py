import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyColor():
  def __init__(self):
    hue_range = np.arange(0, 361, 1)
    hue = ctrl.Antecedent(hue_range, 'hue')
    hue['WARM'] = fuzz.gaussmf(hue.universe, 0, 60)
    hue['COOL'] = fuzz.gaussmf(hue.universe, 180, 60)
    hue['WARM_'] = fuzz.gaussmf(hue.universe, 360, 60)

    self.hue_range = hue_range
    self.hue = hue

    saturation = ctrl.Antecedent(np.arange(0, 101, 1), 'saturation')
    saturation['GRAY'] = fuzz.gaussmf(saturation.universe, 0, 10)
    saturation['VERY_FADED'] = fuzz.gaussmf(saturation.universe, 25, 10)
    saturation['FADED'] = fuzz.gaussmf(saturation.universe, 50, 10)
    saturation['SATURATED'] = fuzz.gaussmf(saturation.universe, 75, 10)
    saturation['VERY_SATURATED'] = fuzz.gaussmf(saturation.universe, 100, 10)

    self.saturation = saturation

    value = ctrl.Antecedent(np.arange(0, 101, 1), 'value')
    value['BLACK'] = fuzz.gaussmf(value.universe, 0, 10)
    value['VERY_DARK'] = fuzz.gaussmf(value.universe, 25, 10)
    value['DARK'] = fuzz.gaussmf(value.universe, 50, 10)
    value['BRIGHT'] = fuzz.gaussmf(value.universe, 75, 10)
    value['VERY_BRIGHT'] = fuzz.gaussmf(value.universe, 100, 10)

    self.value = value

    tone_range = np.arange(0, 12, 1)
    tone = ctrl.Consequent(tone_range, 'tone')

    tone['NEUTRAL'] = fuzz.trapmf(tone.universe, [0, 0, 1, 2])
    tone['DARK'] = fuzz.gbellmf(tone.universe, 2, 1, 3)
    tone['BRIGHT'] = fuzz.gbellmf(tone.universe, 4, 1, 9.5)

    self.tone_rage = tone_range
    self.tone = tone

    tone_cs = ctrl.ControlSystem([
      ctrl.Rule(value['BLACK'] | saturation['GRAY'] | saturation['VERY_FADED'],
                tone['NEUTRAL'], 'Dark colors without color (low brightness/dark) considered neutral'),

      ctrl.Rule(value['VERY_DARK'] & saturation['SATURATED'],
                tone['NEUTRAL'], 'Very dark colors with high saturation'),

      ctrl.Rule(value['DARK'] & saturation['FADED'],
                tone['DARK'], 'Dark color with normal saturation'),

      ctrl.Rule(value['DARK'] & saturation['VERY_SATURATED'],
                tone['BRIGHT'], 'Dark color with high saturation'),

      ctrl.Rule(value['BRIGHT'] & saturation['SATURATED'],
                tone['BRIGHT'], 'Bright color with high saturation'),

      ctrl.Rule(value['VERY_BRIGHT'] & saturation['FADED'],
                tone['BRIGHT'], 'Very bright color with some saturation'),

      ctrl.Rule(value['VERY_BRIGHT'] & saturation['VERY_SATURATED'],
                tone['BRIGHT'], 'Very bright color with high saturation'),

      ctrl.Rule(value['VERY_DARK'] & saturation['FADED'],
                tone['NEUTRAL'], 'Very dark color with faded saturation'),
    ])

    self.tone_cs = tone_cs

  def get_membership(self, fuzzy_range, fuzzy_model, crisp_value):
    max_membership = 0
    fuzzy_terms = list(fuzzy_model.terms.keys())
    membership_name = fuzzy_terms[0]
    for i in range(len(fuzzy_terms)):
      temp_memb = fuzz.interp_membership(
        fuzzy_range, fuzzy_model[fuzzy_terms[i]].mf, crisp_value)
      if temp_memb > max_membership:
        max_membership = temp_memb
        membership_name = fuzzy_terms[i]
    return membership_name

  def get_tone(self, saturation, value):
    tone_sim = ctrl.ControlSystemSimulation(self.tone_cs)
    tone_sim.input['saturation'] = saturation
    tone_sim.input['value'] = value
    tone_sim.compute()
    return self.get_membership(self.tone_rage, self.tone, tone_sim.output['tone'])

  def get_temperature(self, hue_val):
    return self.get_membership(self.hue_range, self.hue, hue_val)

  def get_color_description(self, hue, saturation, value):
    tone = self.get_tone(saturation, value)
    temp = self.get_temperature(hue)
    if temp == "WARM_":
      temp = "WARM"
    return (tone, temp)
