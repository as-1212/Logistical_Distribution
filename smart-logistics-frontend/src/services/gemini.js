import { GoogleGenerativeAI } from '@google/generative-ai';

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI('AIzaSyDemoKeyForGoogleSolutionChallenge2026');
const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

export class LogisticsAI {
  static async analyzeSupplyChain(data) {
    const prompt = `
    As a logistics AI expert, analyze this supply chain data and provide actionable insights:
    
    Data: ${JSON.stringify(data)}
    
    Please provide:
    1. Critical regions needing immediate attention
    2. Recommended stock redistribution
    3. Predicted demand trends
    4. Cost optimization opportunities
    
    Format response as JSON with keys: criticalRegions, recommendations, trends, optimizations
    `;
    
    try {
      const result = await model.generateContent(prompt);
      return JSON.parse(result.response.text());
    } catch (error) {
      console.error('Gemini AI Error:', error);
      return { error: 'AI analysis failed' };
    }
  }

  static async answerLogisticsQuestion(question, context) {
    const prompt = `
    You are an intelligent logistics assistant for a supply chain management system.
    
    Context: ${JSON.stringify(context)}
    User Question: "${question}"
    
    Provide a helpful, specific answer about logistics, inventory management, or supply chain optimization.
    Keep responses concise but comprehensive.
    `;
    
    try {
      const result = await model.generateContent(prompt);
      return result.response.text();
    } catch (error) {
      console.error('Gemini AI Error:', error);
      return 'I apologize, I cannot process your request right now.';
    }
  }

  static async generateInsights(kpiData) {
    const prompt = `
    Analyze these logistics KPIs and provide strategic insights:
    
    KPIs: ${JSON.stringify(kpiData)}
    
    Focus on:
    1. Performance trends
    2. Risk factors
    3. Improvement opportunities
    4. SDG impact (waste reduction, efficiency)
    
    Return insights as actionable recommendations.
    `;
    
    try {
      const result = await model.generateContent(prompt);
      return result.response.text();
    } catch (error) {
      console.error('Gemini AI Error:', error);
      return 'Insights generation failed';
    }
  }
}
