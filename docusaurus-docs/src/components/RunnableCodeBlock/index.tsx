import React, { ReactNode } from 'react';
import Runnable from '../Runnable';

interface RunnableCodeBlockProps {
  children: ReactNode;
  vars?: string;
}

// Backward compatibility: RunnableCodeBlock now uses only Runnable
// ClientExample is available separately when needed
export default function RunnableCodeBlock({ children, vars }: RunnableCodeBlockProps) {
  return <Runnable>{children}</Runnable>;
}
