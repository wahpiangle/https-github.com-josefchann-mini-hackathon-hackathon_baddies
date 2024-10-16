import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import TanStackProvider from "@/provider/TanStackProvider";
import { Toaster } from "@/components/ui/toaster"
import { UploadFileProvider } from "@/context/uploadFileContext";
import Header from "@/components/Header";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "CV Analyzer",
  description: "Analyzing CVs with machine learning",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (

    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased flex flex-col justify-between h-screen`}
      >
        <TanStackProvider>
          <UploadFileProvider>
            <Header />
            <div className="text-white flex items-center justify-center flex-col gap-2 h-full px-32">
              {children}
            </div>
          </UploadFileProvider>
          <Toaster />
        </TanStackProvider>
      </body>
    </html>
  );
}
