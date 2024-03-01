import Image from "next/image";
import styles from "./page.module.css";
import { Button, Container, Flex, Heading, Text } from "@radix-ui/themes";
import FarpointLogo from "@/components/FarpointLogo/FarpointLogo";

export default function Home() {
  return (
    <main className={styles.main}>
      <Flex height={"100%"} width={"100%"} justify={"center"} align={"center"} >
        <Flex direction="column" align={"center"} pb="9">
          <FarpointLogo width={50}/>
          <Heading mt="3">Welcome back to FarpointOI</Heading>
          <Text >Login with your google account</Text>
          <Button mt="3" >login</Button>
        </Flex>
      </Flex>
    </main>
  );
}
