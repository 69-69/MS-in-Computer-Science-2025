package com.techelevator.dao;

import com.techelevator.model.CatCard;

import java.util.List;

public interface CatCardDao {

	List<CatCard> getCatCards();

	CatCard getCatCardById(int id);

	void createCatCard(CatCard catCard);

	void updateCatCard(CatCard card);

	void deleteCatCardById(int id);

}
