// Types for AI Agent integration
export interface QueryRequest {
  query: string;
  max_tokens?: number;
  temperature?: number;
  metadata?: Record<string, any>;
}

export interface AgentResponse {
  response_id: string;
  query: string;
  answer: string;
  sources: string[];
  confidence_score: number;
  processing_time_ms: number;
  retrieval_context: string[];
  timestamp: string;
  metadata: Record<string, any>;
}

export interface APIResponse {
  status: string;
  data?: any;
  error?: {
    type: string;
    message: string;
    details: Record<string, any>;
  };
  request_id: string;
  timestamp: string;
}