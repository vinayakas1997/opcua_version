"""
FINS PLC Memory Areas
=====================
This module defines PLC memory area codes for FINS protocol communication.
"""

__version__ = "0.1.0"


class FinsPLCMemoryAreas:
    """
    Hex codes for PLC memory areas.
    
    Each memory area has corresponding hex codes for word access, bit access,
    forced word access and forced bit access. This class provides name-based
    access to them for better code readability.
    """
    
    def __init__(self):
        # CIO (Common I/O) Area
        self.CIO_BIT = b'\x30'
        self.CIO_WORD = b'\xB0'
        self.CIO_BIT_FORCED = b'\x70'
        self.CIO_WORD_FORCED = b'\xF0'
        
        # Work Area
        self.WORK_BIT = b'\x31'
        self.WORK_WORD = b'\xB1'
        self.WORK_BIT_FORCED = b'\x71'
        self.WORK_WORD_FORCED = b'\xF1'
        
        # Holding Area
        self.HOLDING_BIT = b'\x32'
        self.HOLDING_WORD = b'\xB2'
        self.HOLDING_BIT_FORCED = b'\x72'
        self.HOLDING_WORD_FORCED = b'\xF2'
        
        # Auxiliary Area
        self.AUXILIARY_BIT = b'\x33'
        self.AUXILIARY_WORD = b'\xB3'
        
        # Timer and Counter Areas
        self.TIMER_FLAG = b'\x09'
        self.COUNTER_FLAG = b'\x09'
        self.TIMER_FLAG_FORCED = b'\x49'
        self.COUNTER_FLAG_FORCED = b'\x49'
        self.TIMER_WORD = b'\x89'
        self.COUNTER_WORD = b'\x89'
        
        # Data Memory Area
        self.DATA_MEMORY_BIT = b'\x02'
        self.DATA_MEMORY_WORD = b'\x82'
        
        # Extended Memory Areas (EM0-EM9, EMA-EMF)
        self.EM0_BIT = b'\x20'
        self.EM1_BIT = b'\x21'
        self.EM2_BIT = b'\x22'
        self.EM3_BIT = b'\x23'
        self.EM4_BIT = b'\x24'
        self.EM5_BIT = b'\x25'
        self.EM6_BIT = b'\x26'
        self.EM7_BIT = b'\x27'
        self.EM8_BIT = b'\x28'
        self.EM9_BIT = b'\x29'
        self.EMA_BIT = b'\x2A'
        self.EMB_BIT = b'\x2B'
        self.EMC_BIT = b'\x2C'
        self.EMD_BIT = b'\x2D'
        self.EME_BIT = b'\x2E'
        self.EMF_BIT = b'\x2F'
        
        # Extended Memory Areas (EM10-EM18)
        self.EM10_BIT = b'\xE0'
        self.EM11_BIT = b'\xE1'
        self.EM12_BIT = b'\xE2'
        self.EM13_BIT = b'\xE3'
        self.EM14_BIT = b'\xE4'
        self.EM15_BIT = b'\xE5'
        self.EM16_BIT = b'\xE6'
        self.EM17_BIT = b'\xE7'
        self.EM18_BIT = b'\xE8'
        
        # Extended Memory Word Areas (EM0-EM9, EMA-EMF)
        self.EM0_WORD = b'\xA0'
        self.EM1_WORD = b'\xA1'
        self.EM2_WORD = b'\xA2'
        self.EM3_WORD = b'\xA3'
        self.EM4_WORD = b'\xA4'
        self.EM5_WORD = b'\xA5'
        self.EM6_WORD = b'\xA6'
        self.EM7_WORD = b'\xA7'
        self.EM8_WORD = b'\xA8'
        self.EM9_WORD = b'\xA9'
        self.EMA_WORD = b'\xAA'
        self.EMB_WORD = b'\xAB'
        self.EMC_WORD = b'\xAC'
        self.EMD_WORD = b'\xAD'
        self.EME_WORD = b'\xAE'
        self.EMF_WORD = b'\xAF'
        
        # Extended Memory Word Areas (EM10-EM18)
        self.EM10_WORD = b'\x60'
        self.EM11_WORD = b'\x61'
        self.EM12_WORD = b'\x62'
        self.EM13_WORD = b'\x63'
        self.EM14_WORD = b'\x64'
        self.EM15_WORD = b'\x65'
        self.EM16_WORD = b'\x66'
        self.EM17_WORD = b'\x67'
        self.EM18_WORD = b'\x68'
        
        # Current Bank Areas
        self.EM_CURR_BANK_BIT = b'\x0A'
        self.EM_CURR_BANK_WORD = b'\x98'
        self.EM_CURR_BANK_NUMBER = b'\xBC'
        
        # Task and System Areas
        self.TASK_FLAG_BIT = b'\x06'
        self.TASK_FLAG_STATUS = b'\x46'
        self.INDEX_REGISTER = b'\xDC'
        self.DATA_REGISTER = b'\xBC'
        self.CLOCK_PULSES = b'\x07'
        self.CONDITION_FLAGS = b'\x07'
    
    def get_memory_area_name(self, area_code: bytes) -> str:
        """
        Get the human-readable name for a memory area code.
        
        Args:
            area_code: The memory area code bytes
            
        Returns:
            String name of the memory area or 'UNKNOWN' if not found
        """
        for attr_name in dir(self):
            if not attr_name.startswith('_') and attr_name != 'get_memory_area_name':
                if getattr(self, attr_name) == area_code:
                    return attr_name
        return 'UNKNOWN'
    
    def is_bit_area(self, area_code: bytes) -> bool:
        """
        Check if the area code represents a bit-accessible area.
        
        Args:
            area_code: The memory area code bytes
            
        Returns:
            True if bit area, False otherwise
        """
        bit_areas = [
            self.CIO_BIT, self.WORK_BIT, self.HOLDING_BIT, self.AUXILIARY_BIT,
            self.CIO_BIT_FORCED, self.WORK_BIT_FORCED, self.HOLDING_BIT_FORCED,
            self.TIMER_FLAG, self.COUNTER_FLAG, self.TIMER_FLAG_FORCED, 
            self.COUNTER_FLAG_FORCED, self.DATA_MEMORY_BIT
        ]
        # Add all EM bit areas
        bit_areas.extend([getattr(self, attr) for attr in dir(self) 
                         if attr.endswith('_BIT') and not attr.startswith('_')])
        
        return area_code in bit_areas
    
    def is_word_area(self, area_code: bytes) -> bool:
        """
        Check if the area code represents a word-accessible area.
        
        Args:
            area_code: The memory area code bytes
            
        Returns:
            True if word area, False otherwise
        """
        word_areas = [
            self.CIO_WORD, self.WORK_WORD, self.HOLDING_WORD, self.AUXILIARY_WORD,
            self.CIO_WORD_FORCED, self.WORK_WORD_FORCED, self.HOLDING_WORD_FORCED,
            self.TIMER_WORD, self.COUNTER_WORD, self.DATA_MEMORY_WORD
        ]
        # Add all EM word areas
        word_areas.extend([getattr(self, attr) for attr in dir(self) 
                          if attr.endswith('_WORD') and not attr.startswith('_')])
        
        return area_code in word_areas
