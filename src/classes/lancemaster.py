"""
Actions & Buff bodies of lancemaster(Graivier)
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks, ticks_to_seconds
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 난무/집중 버프 효과 증가 특화 계수
SPEC_COEF_1 = 1 / 13.706 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  # 청룡진 치적 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 6,
    'priority': 7,
  },
  # 스탠스 버프(기본)
  'Stance_Buff_Default': {
    'name': 'stance_buff',
    'buff_type': 'stat',
    'effect': 'stance_buff_default',
    'duration': 12,
    'priority': 9,
  },
  # 스탠스 버프(절정)
  'Stance_Buff_Pinnacle_3': {
    'name': 'stance_buff',
    'buff_type': 'stat',
    'effect': 'stance_buff_pinnacle_3',
    'duration': 12,
    'priority': 9,
  },
  # 절정 확인용 더미 버프
  'Pinnacle_Enabled_3': {
    'name': 'pinnacle_enabled_3',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  # 절제 버프
  'Control_3': {
    'name': 'control_3',
    'buff_type': 'stat',
    'effect': 'control_3',
    'duration': 999999,
    'priority': 7,
  },
}

######## Finalize Skill #########
# finalize skill by tripod and rune
def finalize_skill(skill: Skill):
  name  = skill.get_attribute('name')
  tripod = skill.get_attribute('tripod')
  rune = skill.get_attribute('rune')
  # connect actions
  if name == '스탠스 변경':
    skill.triggered_actions.append('activate_stance_buff')
  # apply tripods
  if name == '청룡진':
    skill.triggered_actions.append('activate_synergy')

######## Actions #########
# 치적 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '청룡진':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], skill_on_use)

# 치적 시너지 등록
def activate_stance_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '스탠스 변경':
    if buff_manager.is_buff_exists('pinnacle_enabled_3'):
      buff_manager.register_buff(CLASS_BUFF_DICT['Stance_Buff_Pinnacle_3'], skill_on_use)
    else:
      buff_manager.register_buff(CLASS_BUFF_DICT['Stance_Buff_Default'], skill_on_use)

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    
# 청룡진 치적 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
  s_acr = skill.get_attribute('additional_crit_rate')
  skill.update_attribute('additional_crit_rate', s_acr + 0.18)

# 기본 난무/집중 버프, 스킬에 맞게 상시 3레벨 가정, 각성기는 난무 취급
# 난무는 20초, 집중은 12초이나 12초로 통일, 난무에서 12초 이상 유지시 확인 필요
def stance_buff_default(character: CharacterLayer, skill: Skill, buff: Buff):
  s = character.get_attribute('specialization')
  buff_multiplier = 1 + (s * SPEC_COEF_1)
  s_dm = skill.get_attribute('damage_multiplier')
  s_acr = skill.get_attribute('additional_crit_rate')
  s_acd = skill.get_attribute('additional_crit_damage')
  c_ms = character.get_attribute('movement_speed')
  c_as = character.get_attribute('attack_speed')
  if (skill.get_attribute('identity_type') == 'Flurry'
      or skill.get_attribute('identity_type') == 'Awakening'
      or skill.get_attribute('identity_type') == None):
    skill.update_attribute('damage_multiplier', s_dm * (1 + (0.10 * buff_multiplier)))
    skill.update_attribute('additional_crit_rate', s_acr + 0.15 * buff_multiplier)
    character.update_attribute('attack_speed', c_as + 0.10 * buff_multiplier)
  elif skill.get_attribute('identity_type') == 'Focus':
    skill.update_attribute('damage_multiplier', s_dm * (1 + (0.10 * buff_multiplier)))
    skill.update_attribute('additional_crit_damage', s_acd + 0.25 * buff_multiplier)
    character.update_attribute('movement_speed', c_ms + 0.15 * buff_multiplier)

# 난무/집중 절정3 적용시 버프
def stance_buff_pinnacle_3(character: CharacterLayer, skill: Skill, buff: Buff):
  s = character.get_attribute('specialization')
  buff_multiplier = 1 + (s * SPEC_COEF_1)
  s_dm = skill.get_attribute('damage_multiplier')
  s_acr = skill.get_attribute('additional_crit_rate')
  s_acd = skill.get_attribute('additional_crit_damage')
  c_ms = character.get_attribute('movement_speed')
  c_as = character.get_attribute('attack_speed')
  if (skill.get_attribute('identity_type') == 'Flurry'
      or skill.get_attribute('identity_type') == 'Awakening'
      or skill.get_attribute('identity_type') == None):
    skill.update_attribute('damage_multiplier', s_dm * (1 + (0.17 * buff_multiplier)))
    skill.update_attribute('additional_crit_rate', s_acr + 0.25 * buff_multiplier)
    character.update_attribute('attack_speed', c_as + 0.15 * buff_multiplier)
  elif skill.get_attribute('identity_type') == 'Focus':
    skill.update_attribute('damage_multiplier', s_dm * (1 + (0.22 * buff_multiplier)))
    skill.update_attribute('additional_crit_damage', s_acd + 0.50 * buff_multiplier)
    character.update_attribute('movement_speed', c_ms + 0.15 * buff_multiplier)

# 절제 적용 버프
def control_3(character: CharacterLayer, skill: Skill, buff: Buff):
  s_dm = skill.get_attribute('damage_multiplier')
  if skill.get_attribute('identity_type') == 'Flurry':
    skill.update_attribute('damage_multiplier', s_dm * 1.40)
