package com.assigndevelopers;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
//import java.util.ArrayList;
//import java.util.Collections;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
//import java.util.stream.Collectors;

public class Peer {
    private final String peerName;
    private ServerSocket serverSocket;
    // private final List<PeerConnection> connections = new ArrayList<>();
    // Steve-Use synchronizedList to avoid ConcurrentModificationException
    //private final List<PeerConnection> connections = Collections.synchronizedList(new ArrayList<>());
    private final CopyOnWriteArrayList<PeerConnection> connections = new CopyOnWriteArrayList<>();
    private final CommunicationService communicationService;

    public Peer(String peerName) {
        this.peerName = peerName;
        this.communicationService = new CommunicationService(this);
    }

    public String getPeerName() {
        return peerName;
    }

    public void startServer(int port) throws IOException {
        serverSocket = new ServerSocket(port);
        System.out.println(peerName + " is listening on port " + port);
        String addr = serverSocket.getInetAddress().getHostAddress();
        System.out.println("Peers can connect via - IP: " + addr + ", Port: " + port);
        new Thread(this::listenForConnections).start();
    }

    public void connectToPeer(String serverAddress, int serverPort) throws IOException {
        Socket socket = new Socket(serverAddress, serverPort);
        PeerConnection connection = new PeerConnection(socket, communicationService, this);
        connections.add(connection);
        new Thread(connection).start();
        System.out.println("Connected to peer at " + serverAddress + ":" + serverPort);
    }

    public void listenForConnections() {
        while (true) {
            try {
                Socket clientSocket = serverSocket.accept();
                PeerConnection connection = new PeerConnection(clientSocket, communicationService, this);
                connections.add(connection);
                new Thread(connection).start();
                // Notify the server about the new peer
                // System.out.println("Connected Peer(s): [" + getConnectedPeers() + "]");
            } catch (IOException e) {
                System.err.println("Error accepting connection: " + e.getMessage());
            }
        }
    }

    public List<PeerConnection> getConnections() {
        return connections;
    }

    // Steve-Use synchronizedList to avoid ConcurrentModificationException
    public String getConnectedPeers() {
        StringBuilder peerList = new StringBuilder();
        for (PeerConnection connection : connections) {
            peerList.append(connection.getSocket().getInetAddress().getHostAddress())
                    .append(":").append(connection.getSocket().getPort()).append(", ");
        }
        return !peerList.isEmpty() ? peerList.substring(0, peerList.length() - 2) : "No connected peers";
    }

    public void closeAllConnections() {
        for (PeerConnection connection : connections) {
            try {
                connection.getSocket().close();
            } catch (IOException e) {
                System.err.println("Error closing connection: " + e.getMessage());
            }
        }
        connections.clear();
        System.out.println("A Peer has disconnected.");
    }

    // Steve-Notify Peer to remove connection
    public void removeConnection(PeerConnection connection) {
        synchronized (connections) {
            connections.remove(connection);
        }
        System.out.println("A Peer has disconnected.");
    }

    public void closeServer() {
        try {
            if (serverSocket != null && !serverSocket.isClosed()) {
                serverSocket.close();
                System.out.println(peerName + " has stopped listening for connections");
            }
        } catch (IOException e) {
            System.err.println("Error closing server: " + e.getMessage());
        }
    }
}
