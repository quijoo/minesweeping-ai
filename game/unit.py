# Unit 类主要实现单元格的状态的管理
# 1. 是否有雷
# 2. 是否可见
# 3. 是否被标记
# 4. 无雷则计算周围雷的数量（先实现不做预计算的版本, 之后可以优化）

# 显示状态
# 1. 游戏结束可见状态
# 1.1 有雷 && 被标记 -> 绿色*
# 1.2 无雷 && 被标记 -> 标记
# 1.3 有雷 && 未标记 -> 红色*
# 1.4 无雷 && 未标记 -> 默认
# 2. 游戏进行状态
# 分为 checked && unchecked
# 2.1  有雷 && 被标记 -> 标记
# 2.2  无雷 && 被标记 -> 标记
# 2.3  有雷 && 未标记 -> 默认
# 2.4  无雷 && 未标记 -> 默认

from game.defines import *


class CUnit:

    def  __init__(self, bBoom:bool):
        self.m_Boom = bBoom
        self.m_State = UNIT_UNKNOWN
        self.m_BoomCount = 0

    def __repr__(self):
        if self.m_State == UNIT_NUM:
            return self.m_BoomCount
        else:
            return self.m_State

    def __str__(self):
        if self.m_State == UNIT_NUM:
            return str(self.m_BoomCount)
        
        elif self.m_State == UNIT_UNKNOWN:
            return DISPLAY_UNKNOWN
        
        elif self.m_State == UNIT_BOOM:
            return DISPLAY_FLAG
        
        elif self.m_State == UNIT_EMPTY:
            return DISPLAY_EMPTY
        
        elif self.m_State == UNIT_SAFE:
            return DISPLAY_UNKNOWN
