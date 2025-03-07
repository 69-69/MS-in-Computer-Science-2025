package com.assigndevelopers;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class PeerConnection implements Runnable {
    private final Socket socket;
    private final BufferedReader in;
    private final PrintWriter out;
    private final CommunicationService communicationService;
    private final Peer peer;

    public PeerConnection(Socket socket, CommunicationService communicationService, Peer peer) throws IOException {
        this.peer = peer;
        this.socket = socket;
        this.in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        this.out = new PrintWriter(socket.getOutputStream(), true);
        this.communicationService = communicationService;
    }

    @Override
    public void run() {
        try {
            String receivedMessage;
            while ((receivedMessage = this.in.readLine()) != null) {
                if (receivedMessage.equalsIgnoreCase("PEER_EXIT")) {
                    System.out.println(communicationService.getPeerName() + " has exited from the chat.");
                    break; // Stop listening for messages from this peer
                }
                communicationService.handleIncomingMessage(receivedMessage);
            }
        } catch (IOException e) {
            System.err.println("Status: " + e.getMessage());
        } finally {
            closeConnection();
            // Steve-Notify Peer to remove connection
            this.peer.removeConnection(this);
        }
    }

    public void sendMessage(String message) {
        this.out.println(message); // Send the message to the other peer
    }

    public Socket getSocket() {
        return this.socket;
    }

    private void closeConnection() {
        try {
            socket.close();
        } catch (IOException e) {
            System.err.println("Error closing peer connection: " + e.getMessage());
        }
    }
}
