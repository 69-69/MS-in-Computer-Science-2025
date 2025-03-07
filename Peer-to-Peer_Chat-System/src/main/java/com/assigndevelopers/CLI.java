package com.assigndevelopers;

import java.io.IOException;
import java.util.List;
import java.util.Scanner;

public class CLI {
    private final Peer peer;
    private final Scanner scanner;
    private final CommunicationService communicationService;
    private final String isServer;

    public CLI(Peer peer, Scanner scanner, String isServer) {
        this.peer = peer;
        this.scanner = scanner;
        this.communicationService = new CommunicationService(peer);
        this.isServer = isServer;
    }

    public void start() {
        try {
            if (this.isServer.equalsIgnoreCase("y")) {
                startAsServer();
            } else {
                startAsClient();
            }
        } catch (IOException e) {
            System.err.println("Error starting the peer: " + e.getMessage());
        } finally {
            cleanUp();
        }
    }

    public void handleMessageInput(String tag) {

        while (true) {
            System.out.println(tag + " Enter message (or 'EXIT' to quit, 'LIST' to view peers):");
            String message = this.scanner.nextLine();

            if (message.equalsIgnoreCase("EXIT")) {
                this.communicationService.sendMessageToAllPeers("PEER_EXIT");
                break;
            } else if (message.equalsIgnoreCase("LIST")) {
                 System.out.println("Connected peers: " + getConnectedPeers());
                continue;
            }
            this.communicationService.sendMessageToAllPeers(message);
        }
    }

    private void startAsServer() throws IOException {
        int port = 0;
        while (true) {
            System.out.print("Enter port to listen on: ");
            if (scanner.hasNextInt()) {
                port = this.scanner.nextInt();
                this.scanner.nextLine(); // Consume newline
                break;  // Exit loop when valid input is received
            } else {
                System.out.println("Invalid input. Please enter a valid Port number.");
                this.scanner.nextLine(); // Clear the invalid input
            }
        }

        this.peer.startServer(port);
        // Show connected peers
        // System.out.println("Connected peers: " + getConnectedPeers());

        startMessageListener();

        this.handleMessageInput("[Peers]");
    }

    private void startAsClient() throws IOException {
        System.out.print("Enter the peer's IP address to connect to: ");
        String ip = this.scanner.nextLine();
        System.out.print("Enter the peer's port to connect to: ");
        int port = this.scanner.nextInt();
        this.scanner.nextLine(); // Consume newline
        this.peer.connectToPeer(ip, port);
        // Show connected peers
        // System.out.println("Connected peers: " + getConnectedPeers());

        startMessageListener();

        this.handleMessageInput("[Peer]");
    }

    private void startMessageListener() {
        new Thread(() -> {
            while (true) {
                for (PeerConnection connection : this.peer.getConnections()) {
                    try {
                        String receivedMessage = this.communicationService.receiveMessage(connection);
                        if (receivedMessage != null) {
                            System.out.println(receivedMessage);
                        }
                    } catch (IOException e) {
                        System.err.println("SOCKET CLOSED" /*e.getMessage()*/);
                        peer.getConnections().remove(connection); // Steve-Safe removal
                        break;
                    }
                }
            }
        }).start();
    }

    private String getConnectedPeers() {
        String connectedPeers = this.peer.getConnectedPeers();
        String p = connectedPeers.isEmpty() ? "No connected peers" : connectedPeers;
        return "[" + p + "]";
    }

    private void cleanUp() {
        this.peer.closeAllConnections();
        if (this.isServer.equalsIgnoreCase("y")) {
            this.peer.closeServer();
        }
        System.out.println("EXITING...");
    }
}
