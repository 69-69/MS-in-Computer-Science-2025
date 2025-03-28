package com.techelevator.controller;

import com.techelevator.exception.DaoException;
import com.techelevator.model.CatCard;
import com.techelevator.dao.CatCardDao;
import com.techelevator.model.CatFact;
import com.techelevator.model.CatPic;
import com.techelevator.services.CatFactService;
import com.techelevator.services.CatPicService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/cards")
public class CatController {

    private CatCardDao catCardDao;
    private CatFactService catFactService;
    private CatPicService catPicService;

    public CatController(CatCardDao catCardDao, CatFactService catFactService, CatPicService catPicService) {
        this.catCardDao = catCardDao;
        this.catFactService = catFactService;
        this.catPicService = catPicService;
    }

    /*
        GET /api/cards: Provides a list of all Cat Cards in the user's collection.
        GET /api/cards/{id}: Provides a Cat Card with the given ID.
        GET /api/cards/random: Provides a new, randomly created Cat Card containing information from the cat fact and picture services.
        POST /api/cards: Saves a card to the user's collection.
        PUT /api/cards/{id}: Updates a card in the user's collection.
        DELETE /api/cards/{id}: Removes a card from the user's collection.
    */

    // GET /api/cards: Provides a list of all Cat Cards in the user's collection.
    @RequestMapping(path = "", method = RequestMethod.GET)
    public List<CatCard> getAllCards() {
        try {
            return catCardDao.getCatCards();
        } catch (DaoException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
        }
        //Need to fix this.
    }

    // GET /api/cards/{id}: Provides a Cat Card with the given ID.
    @RequestMapping(path = "/{id}", method = RequestMethod.GET)
    public CatCard getIndividualCard(@PathVariable int id) {

        CatCard catCard;
        try {
            catCard = catCardDao.getCatCardById(id);
        } catch (DaoException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
        }

        if (catCard == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "CatCard not found");
        }
        return catCard;
    }

    // GET /api/cards/random: Provides a new, randomly created Cat Card containing information from the cat fact and picture services.
    @RequestMapping(path = "/random", method = RequestMethod.GET)
    //Fix 4: Need to implement the path to return the cat card information.
    public CatCard makeNewCard() {
        //Fix 5: Need to fix the catFact logic.
        CatFact f = catFactService.getFact();
        CatPic p = catPicService.getPic();
        CatCard c = new CatCard();

        c.setCatFact(f.getFact());
        c.setImgUrl(p.getFile());

        return c;
    }

    // POST /api/cards: Saves a card to the user's collection.
    @ResponseStatus(HttpStatus.CREATED)
    @RequestMapping(path = "", method = RequestMethod.POST)
    public void saveNewCard(@Valid @RequestBody CatCard incomingCard) {
        //Fix 6:   Need to fix this
        catCardDao.createCatCard(incomingCard);
    }

    // PUT /api/cards/{id}: Updates a card in the user's collection.
    @ResponseStatus(HttpStatus.OK)
    @RequestMapping(path = "/{id}", method = RequestMethod.PUT)
    public void updateExistingCard(@Valid @RequestBody CatCard changedCard, @PathVariable int id) {
        // The id on the URL takes precedence over the one in the payload, if any

        //Fix 7:     Need to fix this
        changedCard.setCatCardId(id);
        catCardDao.updateCatCard(changedCard);
    }

    // DELETE /api/cards/{id}: Removes a card from the user's collection.
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @RequestMapping(path = "/{id}", method = RequestMethod.DELETE)
    public void deleteExistingCard(@PathVariable int id) {
        //Fix 8: Need to fix this.
        catCardDao.deleteCatCardById(id);
    }
}
