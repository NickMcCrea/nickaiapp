// SocketClient.ts
import io, { Socket } from 'socket.io-client';
import { EventEmitter } from 'events';

class SocketClient extends EventEmitter {
  private socket!: Socket;

  constructor(apiUrl: string) {
    super();
    this.connectSocket(apiUrl);
  }

  private connectSocket = (apiUrl: string) => {
    this.socket = io(apiUrl);

    // Generic event listener that re-emits all received events
    this.socket.onAny((event, ...args) => {
      this.emit(event, ...args);
    });
  };

  // Subscribe to a specific event
  subscribe = (event: string, listener: (...args: any[]) => void) => {
    this.on(event, listener);
  };

  // Method to send a message via WebSocket
  sendSocketMessage = (event: string, message: any) => {
    this.socket.emit(event, message);
  };

  // Cleanup method
  cleanup = () => {
    this.socket.removeAllListeners();
    this.socket.disconnect();
  };
}

export default SocketClient;
