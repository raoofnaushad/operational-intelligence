import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import '@radix-ui/themes/styles.css';
import { Theme } from '@radix-ui/themes';
import { GoogleOAuthProvider } from "@react-oauth/google";
import { UserContextProvider } from "@/context/UserContext";
import { cookies } from "next/headers";
import { getCurrentUser } from "@/lib/api";
import { IUser } from "@/types/User";

const inter = Inter({ subsets: ["latin"] });

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID as string

export const metadata: Metadata = {
  title: "FarpointOI",
  description: "FarpointOI",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  let user: IUser|null = null
  const c = cookies().toString()

  try {
    const u = await getCurrentUser(c)
    if (u) user = u
  } catch(e) {
    console.error(e)
  }

  return (
    <html lang="en">
      <body className={inter.className}>
        <Theme>
          <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
            <UserContextProvider initialValue={user}>
              {children}
            </UserContextProvider>
          </GoogleOAuthProvider>
        </Theme>
      </body>
    </html>
  );
}
