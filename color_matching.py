class ColorMatching():
  def __init__(self, color_descriptions):
    self.color_descriptions = color_descriptions

  def rule_basic(self):
    """
    Basic outfit follow these rules
    - No more than one bright color tone
    - No high contrast between colors (bright warm + dark cool)
    - Any number of neutral color tone can fit anywhere
    """

    bright_count = 0

    for [tone, _] in self.color_descriptions:
      if tone == 'BRIGHT':
        bright_count += 1

    # TODO: Check for high contrast

    return bright_count <= 1

  def rule_neutral(self):
    """
    Neutral outfit follow these rules
    - Only neutral color tone
    """

    for [tone, _] in self.color_descriptions:
      if tone != 'NEUTRAL':
        return False

    return True

  def rule_analogous(self):
    """
    Analogous outfit follow these rules
    - All colors must be within the same temp.
    - Any number of neutral color tone
    """

    first_color_temp = self.color_descriptions[0][1]
    for [_, temp] in self.color_descriptions[1:]:
      if first_color_temp != temp:
        return False

    return True

  def rule_contrast(self):
    """
    Contrast outfit follow these rules
    - At least one warm color temp
    - Both dark and bright color tone present
    """

    warm_count = 0
    dark_count = 0
    bright_count = 0

    for [tone, temp] in self.color_descriptions:
      if temp == 'WARM':
        warm_count += 1
      if tone == 'DARK':
        dark_count += 1
      if tone == 'BRIGHT':
        bright_count += 1

    return warm_count > 0 and dark_count > 0 and bright_count > 0

  def rule_bright_summer(self):
    """
    Bright summer outfit follow these rules
    - Ignore neutral color tone
    - At least two warm color temp
    - At most one dark color tone
    - At least one bright color tone
    """

    warm_count = 0
    dark_count = 0
    bright_count = 0

    for [tone, temp] in self.color_descriptions:
      if tone == 'NEUTRAL':
        continue
      if temp == 'WARM':
        warm_count += 1
      if tone == 'DARK':
        dark_count += 1
      if tone == 'BRIGHT':
        bright_count += 1

    return warm_count >= 2 and dark_count <= 1 and bright_count >= 1

  def rule_dark_winter(self):
    """
    Dark winter outfit follow these rules
    - Ignore neutral color tone
    - At least one dark color tone
    - No bright color tone
    """

    dark_count = 0
    bright_count = 0

    for [tone, _] in self.color_descriptions:
      if tone == 'NEUTRAL':
        continue
      if tone == 'DARK':
        dark_count += 1
      if tone == 'BRIGHT':
        bright_count += 1

    return dark_count >= 1 and bright_count == 0

  def get_all_valid_matches(self):
    rules = {
      "Basic": self.rule_basic,
      "Neutral": self.rule_neutral,
      "Analogous": self.rule_analogous,
      "Summer": self.rule_bright_summer,
      "Winter": self.rule_dark_winter
    }

    valid_matches = []
    for key in rules:
      if rules[key]():
        valid_matches.append(key)

    return valid_matches
