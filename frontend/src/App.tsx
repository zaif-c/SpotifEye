import { MantineProvider } from '@mantine/core';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Header } from './components/Header';
import { UserProfile } from './components/UserProfile';
import { Callback } from './pages/Callback';
import { useAuth } from './hooks/useAuth';
import { Container, Text, Button, Center, Stack, Image, Paper, Title } from '@mantine/core';
import { auth } from './services/api';
import '@mantine/core/styles.css';
import { LoadingScreen } from './components/LoadingScreen';

function Home() {
  const { token, error, loading } = useAuth();

  if (loading) {
    return <LoadingScreen message="Checking authentication..." />;
  }

  if (error) {
    return (
      <Container size="sm" py="xl">
        <Center>
          <Stack align="center" gap="xl">
            <Text color="red" size="xl">
              Error: {error}
            </Text>
            <Button onClick={() => auth.login()} size="lg">
              Try Again
            </Button>
          </Stack>
        </Center>
      </Container>
    );
  }

  if (token) {
    return <UserProfile />;
  }

  return (
    <Container size="sm" style={{ 
      minHeight: 'calc(100vh - 60px)', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center' 
    }}>
      <Paper shadow="md" p="xl" radius="md" withBorder style={{ width: '100%' }}>
        <Stack align="center" gap="xl">
          <Stack gap={0} align="center">
            <Image
              src="/logo.png"
              alt="SpotifEye Logo"
              width={120}
              height={120}
              fit="contain"
              style={{ 
                marginBottom: '-1.5rem',
                objectFit: 'contain',
                objectPosition: 'center',
                padding: '0.2rem'
              }}
            />
            <Title order={1} size="h2">SpotifEye</Title>
          </Stack>
          <Text color="dimmed" ta="center" size="lg">
            Connect with Spotify to view your music statistics and discover new insights about your listening habits.
          </Text>
          <Button 
            onClick={() => auth.login()} 
            size="lg"
            variant="gradient"
            gradient={{ from: '#1DB954', to: '#1ed760' }}
            radius="xl"
            fullWidth
          >
            Login with Spotify
          </Button>
        </Stack>
      </Paper>
    </Container>
  );
}

function App() {
  return (
    <MantineProvider>
      <Router>
        <Header />
        <Routes>
          <Route path="/callback" element={<Callback />} />
          <Route path="/" element={<Home />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </MantineProvider>
  );
}

export default App;
