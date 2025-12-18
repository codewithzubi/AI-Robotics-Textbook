import React from 'react';
import Layout from '@theme/Layout';
import AIQueryInterface from '../components/AIQueryInterface/AIQueryInterface';

export default function AIPage(): React.Component {
  return (
    <Layout title="AI Assistant" description="Ask questions about the AI Robotics textbook">
      <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <h1>AI Assistant for AI Robotics Textbook</h1>
        <p>Ask questions about the content of the textbook and get AI-powered answers based on the material.</p>

        <AIQueryInterface />
      </div>
    </Layout>
  );
}