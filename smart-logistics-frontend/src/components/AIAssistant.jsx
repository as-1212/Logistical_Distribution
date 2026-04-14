import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Sparkles, AlertTriangle, TrendingUp, Package } from 'lucide-react';
import { LogisticsAI } from '../services/gemini';

const AIAssistant = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: '🤖 Hello! I\'m your AI logistics assistant. I can help you with:\n\n• Stock optimization\n• Demand analysis\n• Supply chain insights\n• Risk assessment\n\nWhat would you like to know?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [suggestions] = useState([
    'Which state needs stock urgently?',
    'Where should I send inventory?',
    'Summarize supply issues',
    'Predict demand for next month',
    'Optimize distribution routes'
  ]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: messageText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      // Get context from current dashboard data
      const context = {
        totalOrders: '12,340',
        revenue: '8.4M',
        alerts: 23,
        inTransit: 340
      };

      const aiResponse = await LogisticsAI.answerLogisticsQuestion(messageText, context);
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: aiResponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('AI Response Error:', error);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(input);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="bg-card-bg rounded-2xl shadow-card p-6 h-96 flex flex-col"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-info rounded-xl flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-text-primary font-semibold">AI Logistics Assistant</h3>
            <p className="text-text-secondary text-xs">Powered by Gemini</p>
          </div>
        </div>
        <div className="flex items-center space-x-1">
          <Sparkles className="w-4 h-4 text-warning animate-pulse" />
          <span className="text-xs text-text-secondary">Online</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-3">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-xs lg:max-w-md ${
                message.type === 'user' 
                  ? 'bg-primary text-white' 
                  : 'bg-slate-700 text-text-primary'
              } rounded-2xl px-4 py-3`}>
                <div className="flex items-start space-x-2">
                  {message.type === 'bot' && (
                    <Bot className="w-4 h-4 text-info mt-1 flex-shrink-0" />
                  )}
                  <div className="flex-1">
                    <p className="text-sm whitespace-pre-line">{message.content}</p>
                    <p className="text-xs opacity-70 mt-1">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                  {message.type === 'user' && (
                    <User className="w-4 h-4 text-white mt-1 flex-shrink-0" />
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {isTyping && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="bg-slate-700 text-text-primary rounded-2xl px-4 py-3">
              <div className="flex items-center space-x-2">
                <Bot className="w-4 h-4 text-info" />
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-text-secondary rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-text-secondary rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                  <div className="w-2 h-2 bg-text-secondary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                </div>
              </div>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions */}
      <div className="mb-3">
        <p className="text-xs text-text-secondary mb-2">Quick Questions:</p>
        <div className="flex flex-wrap gap-2">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSendMessage(suggestion)}
              className="text-xs bg-slate-700 hover:bg-slate-600 text-text-primary px-3 py-1 rounded-full transition-colors"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="flex items-center space-x-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about logistics, inventory, or supply chain..."
          className="flex-1 bg-slate-700 text-text-primary placeholder-text-muted rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <button
          onClick={() => handleSendMessage(input)}
          disabled={!input.trim() || isTyping}
          className="bg-primary hover:bg-primary/90 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-xl p-3 transition-colors"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </motion.div>
  );
};

export default AIAssistant;
