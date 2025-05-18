import { Container, Group, Button, Text, Stack, Image } from '@mantine/core';
import { useAuth } from '../hooks/useAuth';
import { auth } from '../services/api';

export function Header() {
  const { token } = useAuth();

  const logout = async () => {
    try {
      await auth.logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <Container fluid px={0} py="md">
      <Group justify="space-between" px="xl">
        <Stack gap={0} align="center">
          <Image
            src="/logo.png"
            alt="SpotifEye Logo"
            width={64}
            height={64}
            fit="contain"
            style={{ 
              marginBottom: '-1rem',
              objectFit: 'contain',
              objectPosition: 'center',
              padding: '0.2rem'
            }}
          />
          <Text size="xl" fw={700}>SpotifEye</Text>
        </Stack>
        {token ? (
          <Button onClick={logout} variant="light">
            Logout
          </Button>
        ) : null}
      </Group>
    </Container>
  );
} 