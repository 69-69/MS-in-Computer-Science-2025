package com.techelevator.dao;

import com.techelevator.exception.DaoException;
import com.techelevator.model.CatCard;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.jdbc.CannotGetJdbcConnectionException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.support.rowset.SqlRowSet;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class JdbcCatCardDao implements CatCardDao {

	private JdbcTemplate jdbcTemplate;
	private Logger log = LoggerFactory.getLogger(getClass());

	public JdbcCatCardDao(JdbcTemplate jdbcTemplate) {
		this.jdbcTemplate = jdbcTemplate;
	}

	@Override
	public List<CatCard> getCatCards() {
		List<CatCard> catCards = new ArrayList<>();
		String sql = "SELECT id, img_url, fact, caption FROM catcards";
		try {
			SqlRowSet results = jdbcTemplate.queryForRowSet(sql);
			while (results.next()) {
				CatCard card = mapRowToCard(results);
				catCards.add(card);
			}
		} catch (CannotGetJdbcConnectionException e) {
			throw new DaoException("Unable to connect to server or database", e);
		}
		return catCards;
	}

	@Override
	public CatCard getCatCardById(int id) {
		CatCard card = null;
		String sql = "SELECT id, img_url, fact, caption FROM catcards WHERE id = ?";
		try {
			SqlRowSet results = jdbcTemplate.queryForRowSet(sql, id);
			if (results.next()) {
				card = mapRowToCard(results);
			}
		} catch (CannotGetJdbcConnectionException e) {
			throw new DaoException("Unable to connect to server or database", e);
		}
		return card;
	}

	@Override
	public void updateCatCard(CatCard catCard) {
		CatCard updatedCatCard = null;
		String sql = "UPDATE catcards SET img_url = ?, fact = ?, caption = ? WHERE id = ?";
		try {
			int rowsAffected = jdbcTemplate.update(sql, catCard.getImgUrl(), catCard.getCatFact(), catCard.getCaption(), catCard.getCatCardId());
			if (rowsAffected == 0) {
				throw new DaoException("Zero rows affected, expected at least one");
			}
			updatedCatCard = getCatCardById(catCard.getCatCardId());
		} catch (CannotGetJdbcConnectionException e) {
			throw new DaoException("Unable to connect to server or database", e);
		} catch (DataIntegrityViolationException e) {
			throw new DaoException("Data integrity violation", e);
		}
	}

	@Override
	public void deleteCatCardById(int id) {
		int numberOfRows = 0;
		String sql = "DELETE FROM catcards WHERE id = ?";
		try {
			numberOfRows = jdbcTemplate.update(sql, id);
		} catch (CannotGetJdbcConnectionException e) {
			throw new DaoException("Unable to connect to server or database", e);
		} catch (DataIntegrityViolationException e) {
			throw new DaoException("Data integrity violation", e);
		}
	}

	@Override
	public void createCatCard(CatCard catCard) {
		CatCard newCatCard = null;
		String sql = "INSERT INTO catcards (img_url, fact, caption) VALUES (?, ?, ?) RETURNING id";
		try {
			int catCardId = jdbcTemplate.queryForObject(sql, int.class, catCard.getImgUrl(), catCard.getCatFact(), catCard.getCaption());
			newCatCard = getCatCardById(catCardId);
		} catch (CannotGetJdbcConnectionException e) {
			throw new DaoException("Unable to connect to server or database", e);
		} catch (DataIntegrityViolationException e) {
			throw new DaoException("Data integrity violation", e);
		}
	}

	private CatCard mapRowToCard(SqlRowSet rs) {
		CatCard cc = new CatCard();
		cc.setCatCardId(rs.getInt("id"));
		cc.setCatFact(rs.getString("fact"));
		cc.setImgUrl(rs.getString("img_url"));
		cc.setCaption(rs.getString("caption"));
		return cc;
	}

}
