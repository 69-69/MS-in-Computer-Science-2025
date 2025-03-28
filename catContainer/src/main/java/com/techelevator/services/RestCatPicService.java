package com.techelevator.services;

import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.client.RestTemplate;

import com.techelevator.model.CatPic;

@Component
public class RestCatPicService implements CatPicService {

    private static final String API_URL = "https://cat-data.netlify.app/api/pictures/random";

    private final RestTemplate restTemplate = new RestTemplate();

    public CatPic getPic() throws RestClientResponseException {
        return restTemplate.getForObject(API_URL, CatPic.class);
    }



}
