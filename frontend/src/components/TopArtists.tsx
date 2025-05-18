import { useEffect, useState } from 'react';
import { Title, Grid, Card, Text, Image, Stack } from '@mantine/core';
import { spotify } from '../services/api';
import { LoadingScreen } from './LoadingScreen';

interface Artist {
  id: string;
  name: string;
  images: Array<{ url: string }>;
  genres: string[];
}

interface TopArtistsProps {
  timeRange: string;
}

export function TopArtists({ timeRange }: TopArtistsProps) {
  const [artists, setArtists] = useState<Artist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchArtists = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await spotify.getTopArtists(timeRange);
        setArtists(data);
      } catch (err) {
        console.error('Error fetching top artists:', err);
        setError('Failed to load top artists');
      } finally {
        setLoading(false);
      }
    };

    fetchArtists();
  }, [timeRange]);

  if (loading) {
    return <LoadingScreen message="Loading top artists..." />;
  }

  if (error) {
    return <Text color="red">{error}</Text>;
  }

  return (
    <Stack gap={0}>
      <Title order={2} mb={0}>Your Top Artists</Title>
      <Grid gutter="md" mt="md">
        {artists.map((artist, index) => (
          <Grid.Col key={artist.id} span={{ base: 12, sm: 6, md: 4 }}>
            <Card shadow="sm" padding="lg" radius="md" withBorder h="100%">
              <Card.Section>
                <Image
                  src={artist.images[0]?.url}
                  height={160}
                  alt={artist.name}
                  style={{ objectFit: 'cover' }}
                />
              </Card.Section>

              <Stack mt="md" gap="xs">
                <Text fw={500} size="lg" lineClamp={1}>
                  {index + 1}. {artist.name}
                </Text>
                <Text size="sm" c="dimmed" lineClamp={1} style={{ minHeight: '1.5em' }}>
                  {artist.genres && artist.genres.length > 0 
                    ? artist.genres.slice(0, 2).join(', ')
                    : ' '}
                </Text>
              </Stack>
            </Card>
          </Grid.Col>
        ))}
      </Grid>
    </Stack>
  );
} 