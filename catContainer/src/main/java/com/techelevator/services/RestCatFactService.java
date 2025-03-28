package com.techelevator.services;

import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.client.RestTemplate;

import com.techelevator.model.CatFact;

@Component
public class RestCatFactService implements CatFactService {

    private static final String API_URL = "https://cat-data.netlify.app/api/facts/random";

    private final RestTemplate restTemplate = new RestTemplate();

    public CatFact getFact() throws RestClientResponseException {
        //Fix 2: Need to fix this.
        return restTemplate.getForObject(API_URL, CatFact.class);
    }




}




