'use client';

import { useState, useEffect, useRef } from 'react';
import { HEADER } from '../../layouts/base/main';
import { Box, Container, TextField, Button, Typography, Paper } from '@mui/material';
import BaseLayout from '../../layouts/base';
import ReactMarkdown from 'react-markdown';
import { useSearchParams } from 'next/navigation';

// ----------------------------------------------------------------------

export const metadata = {
  title: 'OpenTCM - Chat',
};

function generateRandomUserId() {
  return Math.random().toString(36).substr(2, 9);
}

export default function ChatView() {
  const [messages, setMessages] = useState([{ role: 'bot', content: '欢迎试用OpenTCM，我可以帮您解答中医相关问题。' }]);
  const [input, setInput] = useState('');
  const [userId, setUserId] = useState('');
  const messagesEndRef = useRef(null);
  const searchParams = useSearchParams();
  const init_query = searchParams.get('query');
  const inited = useRef(false);
  const apiKey = process.env.NEXT_PUBLIC_FASTGPT_API_KEY;
  const currentTimestamp = new Date().getTime().toString();

  useEffect(() => {
    setUserId(generateRandomUserId());
  }, []);

  useEffect(() => {
    if (init_query && !inited.current) {
      inited.current = true;
      handleSendQuery(init_query);
    }
  }, [init_query]);

  const chatId = userId;

  const handleSendQuery = async (query) => {
    const userMessage = { role: 'user', content: query };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    await getGptResponse(query);
  };

  const handleSend = async () => {
    if (input.trim()) {
      const userMessage = { role: 'user', content: input };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInput('');

      await getGptResponse(input);
    }
  };

  const getGptResponse = async (message) => {
    const response = await fetch('https://api.fastgpt.in/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`, // Use environment variable for API key
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chatId: chatId,
        stream: true,
        detail: false,
        variables: {
          uid: userId,
          name: 'OpenTCM',
        },
        messages: [
          {
            content: message,
            role: 'user',
          },
        ],
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let botMessage = { role: 'bot', content: '' };

    setMessages((prevMessages) => [...prevMessages, botMessage]);

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n').filter(line => line.trim() !== '');
      for (const line of lines) {
        if (line.trim() === 'data: [DONE]') {
          return;
        }

        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6));
          const delta = data.choices[0].delta.content || '';
          botMessage.content += delta;
          setMessages((prevMessages) =>
            prevMessages.map((msg, idx) =>
              idx === prevMessages.length - 1 ? botMessage : msg,
            ),
          );
        }
      }
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <BaseLayout hideFooter={true}>
      <Box sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        pt: `${HEADER.H_MOBILE}px`,
        boxSizing: 'border-box',
      }}>
        <Container maxWidth="md" sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, mt: 0, pb: 10 }}>
          <Paper sx={{ flexGrow: 1, p: 2, mb: 2, overflowY: 'auto' }}>
            {messages.map((msg, index) => (
              <Box key={index} sx={{ mb: 2, textAlign: msg.role === 'user' ? 'right' : 'left' }}>
                <Typography variant="body1" sx={{
                  display: 'inline-block',
                  bgcolor: msg.role === 'user' ? 'primary.main' : 'grey.300',
                  color: msg.role === 'user' ? 'white' : 'black',
                  p: 1,
                  borderRadius: 2,
                }}>
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </Typography>
              </Box>
            ))}
            <div ref={messagesEndRef} />
          </Paper>
        </Container>
        <Box sx={{
          position: 'fixed',
          bottom: 0,
          left: 0,
          width: '100%',
          py: 0.5,
          px: 0,
          // boxShadow: '0 -2px 5px rgba(0,0,0,0.1)',
        }}>
          <Container maxWidth="md" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', width: '100%', bgcolor: 'background.default' }}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder="Type your message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    height: '56px',  // Ensure the height matches your design
                  },
                }}
              />
              <Button
                variant="contained"
                sx={{
                  ml: 2,
                  height: '56px',  // Match the TextField height
                  minWidth: 'auto',  // Ensure the button width adjusts based on content
                }}
                onClick={handleSend}
              >
                Send
              </Button>
            </Box>
            <Typography variant="caption" sx={{ mt: 1, textAlign: 'center', width: '100%', color: 'text.secondary' }}>
              Disclaimer: OpenTCM provides TCM knowledge. Consult a healthcare provider for medical advice.
            </Typography>
          </Container>
        </Box>
      </Box>
    </BaseLayout>
  );
}
