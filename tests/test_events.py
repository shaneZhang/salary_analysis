"""
事件总线测试
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.events.event_bus import EventBus, Event, EVENT_TYPES


class TestEventBusExtended(unittest.TestCase):
    """EventBus扩展测试"""
    
    def setUp(self):
        self.eb = EventBus()
    
    def test_event_creation(self):
        """测试事件创建"""
        event = Event('test_type', {'key': 'value'})
        
        self.assertEqual(event.event_type, 'test_type')
        self.assertEqual(event.data['key'], 'value')
        self.assertIsNotNone(event.timestamp)
    
    def test_event_types(self):
        """测试事件类型常量"""
        self.assertIn('DATA_LOADED', EVENT_TYPES)
        self.assertIn('DATA_UPDATED', EVENT_TYPES)
        self.assertIn('STATUS_CHANGED', EVENT_TYPES)
        self.assertIn('ERROR_OCCURRED', EVENT_TYPES)
    
    def test_publish_with_event_object(self):
        """测试发布事件对象"""
        received = []
        
        def handler(event):
            received.append(event)
        
        self.eb.subscribe('test', handler)
        
        event = Event('test', {'data': 'test'})
        self.eb.publish('test', event.data)
        
        self.assertEqual(len(received), 1)
    
    def test_clear_handlers(self):
        """测试清除处理器"""
        def handler1(event):
            pass
        
        def handler2(event):
            pass
        
        self.eb.subscribe('event1', handler1)
        self.eb.subscribe('event2', handler2)
        
        self.eb.clear_handlers()
        
        self.assertEqual(len(self.eb.get_handlers('event1')), 0)
        self.assertEqual(len(self.eb.get_handlers('event2')), 0)
    
    def test_get_history(self):
        """测试获取事件历史"""
        def handler(event):
            pass
        
        self.eb.subscribe('test', handler)
        self.eb.publish('test', {'data': 1})
        self.eb.publish('test', {'data': 2})
        
        history = self.eb.get_history('test')
        
        self.assertEqual(len(history), 2)
    
    def test_get_all_history(self):
        """测试获取所有事件历史"""
        def handler(event):
            pass
        
        self.eb.subscribe('test1', handler)
        self.eb.subscribe('test2', handler)
        
        self.eb.publish('test1', {'data': 1})
        self.eb.publish('test2', {'data': 2})
        
        history = self.eb.get_history()
        
        self.assertEqual(len(history), 2)


if __name__ == '__main__':
    unittest.main()
