import { useEffect, useState } from 'react';
import { Title, Grid, Card, Text, Image, Stack } from '@mantine/core';
import { spotify } from '../services/api';
import { LoadingScreen } from './LoadingScreen';

interface Track {
  id: string;
  name: string;
  artists: Array<{ name: string }>;
  album: {
    name: string;
    images: Array<{ url: string }>;
  };
}

interface TopTracksProps {
  timeRange: string;
}

export function TopTracks({ timeRange }: TopTracksProps) {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTracks = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await spotify.getTopTracks(timeRange);
        setTracks(data);
      } catch (err) {
        console.error('Error fetching top tracks:', err);
        setError('Failed to load top tracks');
      } finally {
        setLoading(false);
      }
    };

    fetchTracks();
  }, [timeRange]);

  if (loading) {
    return <LoadingScreen message="Loading top tracks..." />;
  }

  if (error) {
    return <Text color="red">{error}</Text>;
  }

  return (
    <Stack gap={0}>
      <Title order={2} mb={0}>Your Top Tracks</Title>
      <Grid gutter="md" mt="md">
        {tracks.map((track, index) => (
          <Grid.Col key={track.id} span={{ base: 12, sm: 6, md: 4 }}>
            <Card shadow="sm" padding="lg" radius="md" withBorder h="100%">
              <Card.Section>
                <Image
                  src={track.album.images[0]?.url}
                  height={160}
                  alt={track.album.name}
                  style={{ objectFit: 'cover' }}
                />
              </Card.Section>

              <Stack mt="md" gap="xs">
                <Text fw={500} size="lg" lineClamp={1}>
                  {index + 1}. {track.name}
                </Text>
                <Text size="sm" c="dimmed" lineClamp={1}>
                  {track.artists.map(artist => artist.name).join(', ')}
                </Text>
                <Text size="sm" c="dimmed" lineClamp={1}>
                  {track.album.name}
                </Text>
              </Stack>
            </Card>
          </Grid.Col>
        ))}
      </Grid>
    </Stack>
  );
} 