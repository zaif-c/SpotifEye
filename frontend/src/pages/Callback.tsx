import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Container, Text, Loader, Center } from "@mantine/core";

const API_URL = import.meta.env.VITE_API_URL;

export function Callback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const code = searchParams.get("code");
    const token = searchParams.get("token");

    if (token) {
      // Store the token directly
      localStorage.setItem("token", token);
      navigate("/");
    } else if (code) {
      // Let the backend handle the callback
      window.location.href = `${API_URL}/callback?code=${code}`;
    } else {
      // Handle error case
      const error = searchParams.get("error");
      console.error("Spotify authorization error:", error);
      navigate("/");
    }
  }, [searchParams, navigate]);

  return (
    <Container size="sm" py="xl">
      <Center>
        <Loader size="lg" />
        <Text ml="md">Completing authentication...</Text>
      </Center>
    </Container>
  );
}
 