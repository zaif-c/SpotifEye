import { useEffect, useState } from "react";
import {
  Container,
  Title,
  Text,
  Avatar,
  Group,
  Stack,
  Grid,
  Paper,
  SegmentedControl,
  Select,
} from "@mantine/core";
import { auth } from "../services/api";
import { TopTracks } from "./TopTracks";
import { TopArtists } from "./TopArtists";
import { LoadingScreen } from "./LoadingScreen";

interface User {
  id: string;
  display_name: string;
  images: { url: string }[];
  followers: { total: number };
}

export function UserProfile() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<"tracks" | "artists">("tracks");
  const [timeRange, setTimeRange] = useState<
    "short_term" | "medium_term" | "long_term"
  >("medium_term");

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await auth.getMe();
        setUser(response);
        setError(null);
      } catch (err) {
        console.error("Error fetching user:", err);
        setError("Failed to load profile. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  if (loading) {
    return <LoadingScreen message="Loading profile..." />;
  }

  if (error || !user) {
    return (
      <Container size="lg" py="xl">
        <Text color="red" size="xl" ta="center">
          {error || "Failed to load profile"}
        </Text>
      </Container>
    );
  }

  return (
    <Container fluid px="xl" py="xl">
      <Stack gap="xl">
        <Group>
          <Avatar src={user.images[0]?.url} size="xl" radius="xl" />
          <div>
            <Title order={1}>{user.display_name}</Title>
            <Text size="lg" c="dimmed">
              {user.followers.total.toLocaleString()} followers
            </Text>
          </div>
        </Group>

        <Grid gutter="xl">
          <Grid.Col span={{ base: 12, md: 8 }}>
            {viewMode === "tracks" ? (
              <TopTracks timeRange={timeRange} />
            ) : (
              <TopArtists timeRange={timeRange} />
            )}
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 4 }}>
            <Paper
              p="md"
              withBorder
              style={{
                position: "sticky",
                top: "1rem",
                marginTop: "3.2rem",
              }}
            >
              <Stack gap="md">
                <SegmentedControl
                  value={viewMode}
                  onChange={(value) => setViewMode(value as typeof viewMode)}
                  data={[
                    { label: "Tracks", value: "tracks" },
                    { label: "Artists", value: "artists" },
                  ]}
                  fullWidth
                />
                <Select
                  label="Time Range"
                  value={timeRange}
                  onChange={(value) => setTimeRange(value as typeof timeRange)}
                  data={[
                    { value: "short_term", label: "Last 4 Weeks" },
                    { value: "medium_term", label: "Last 6 Months" },
                    { value: "long_term", label: "All Time" },
                  ]}
                  style={{ width: "100%" }}
                />
              </Stack>
            </Paper>
          </Grid.Col>
        </Grid>
      </Stack>
    </Container>
  );
}
