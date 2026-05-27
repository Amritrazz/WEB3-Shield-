import './globals.css';

export const metadata = {
  title: 'Web3-Shield Dashboard',
  description: 'Real-time Web3 Phishing & Transaction Interception Security Layer',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body style={{ margin: 0, padding: 0, backgroundColor: '#0f172a', color: '#f8fafc' }}>
        {children}
      </body>
    </html>
  );
}
