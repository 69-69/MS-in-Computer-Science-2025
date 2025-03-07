package com.assigndevelopers;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);

        System.out.println("\n--------------------------------------");
        System.out.println("Welcome to Peer-to-Peer Chat System!".toUpperCase());
        System.out.println("--------------------------------------");
        System.out.print("What's your name: ");
        String peerName = scanner.nextLine();

        System.out.print("Do you want to act as a SERVER (y/n)? ");
        String isServer = scanner.nextLine().toLowerCase();

        Peer peer = new Peer(peerName.toUpperCase());
        CLI cli = new CLI(peer, scanner, isServer);
        cli.start();
    }
}
