package com.techelevator.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class CatFact {
    //Fix 3: Need to fix this.

    @JsonProperty("text")
    private String fact;

    public String getFact() {
        return fact;
    }

    public void setFact(String fact) {
        this.fact = fact;
    }
}
