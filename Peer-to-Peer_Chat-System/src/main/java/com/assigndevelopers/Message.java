package com.assigndevelopers;

import java.text.SimpleDateFormat;
import java.util.Date;

public class Message {
    private final String content;
    private final String sender;
    private final long timestamp;
    SimpleDateFormat dt_format = new SimpleDateFormat("MM dd, yy @ HH:mm:ss");

    public Message(String content, String sender) {
        this.content = content;
        this.sender = sender;
        this.timestamp = System.currentTimeMillis();
    }

    public String getContent() {
        return content;
    }

    public String getSender() {
        return sender;
    }

    public long getTimestamp() {
        return timestamp;
    }

    @Override
    public String toString() {
        var date_time = new Date(timestamp);
        return "From: " + sender + " [" + dt_format.format(date_time) + "] - " + content + "...";
    }
}
