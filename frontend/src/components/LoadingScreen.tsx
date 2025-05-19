import { Center, Loader, Text, Stack } from "@mantine/core";

interface LoadingScreenProps {
  message?: string;
}

export function LoadingScreen({ message = "Loading..." }: LoadingScreenProps) {
  return (
    <Center h="100vh">
      <Stack align="center" gap="md">
        <Loader size="lg" />
        <Text size="lg">{message}</Text>
      </Stack>
    </Center>
  );
}
