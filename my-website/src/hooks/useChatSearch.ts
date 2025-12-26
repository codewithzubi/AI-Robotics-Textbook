import { useState, useCallback } from 'react';

// Define a global event system to communicate between search and chat
type ChatEvent = {
  type: 'NEW_QUERY';
  payload: {
    query: string;
  };
};

const eventHandlers: ((event: ChatEvent) => void)[] = [];

export const useChatSearch = () => {
  const [searchQuery, setSearchQuery] = useState<string | null>(null);

  const subscribeToChatEvents = useCallback((handler: (event: ChatEvent) => void) => {
    eventHandlers.push(handler);
    return () => {
      const index = eventHandlers.indexOf(handler);
      if (index > -1) {
        eventHandlers.splice(index, 1);
      }
    };
  }, []);

  const dispatchChatEvent = useCallback((event: ChatEvent) => {
    eventHandlers.forEach(handler => handler(event));
  }, []);

  const performSearch = useCallback((query: string) => {
    // Store the query
    setSearchQuery(query);

    // Dispatch an event to notify the chat interface
    dispatchChatEvent({
      type: 'NEW_QUERY',
      payload: { query }
    });
  }, [dispatchChatEvent]);

  return {
    searchQuery,
    performSearch,
    subscribeToChatEvents
  };
};