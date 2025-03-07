package com.assigndevelopers;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class CommunicationService {
    private final Peer peer;

    public CommunicationService(Peer peer) {
        this.peer = peer;
    }

    public String getPeerName() {
        return peer.getPeerName();
    }

    public void sendMessageToAllPeers(String messageContent) {
        Message message = new Message(messageContent, peer.getPeerName());
        for (PeerConnection connection : peer.getConnections()) {
            connection.sendMessage(message.toString());
        }
    }

    public String receiveMessage(PeerConnection connection) throws IOException {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getSocket().getInputStream()));
            return in.readLine();
        } catch (IOException e) {
            // Steve-Notify Peer to remove connection
            System.err.println("Status: " + e.getMessage());
            this.peer.removeConnection(connection); // Remove the failed connection
            return null;
        }
    }


    public void handleIncomingMessage(String message) {
        if (message.equals("PEER_EXIT")) {
            System.out.println("A peer has exited.");
        } else {
            System.out.println(message);
        }
    }
}
