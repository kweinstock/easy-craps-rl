interface MessageToastProps {
  message: string;
}

export default function MessageToast({ message }: MessageToastProps) {
  return <div className="message-toast">{message}</div>;
}
