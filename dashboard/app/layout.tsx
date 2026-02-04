import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Bioinformatics Pipeline Dashboard",
  description: "Prokaryotic genome assembly analytics and visualization",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
