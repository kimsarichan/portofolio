package com.example.s.cinemasari.model;

import android.os.Parcelable;

/**
 * Created by S on 5/10/2016.
 */
public class ReviewModel {
    private String  author;
    private String content;
    private String url;

    public ReviewModel(String author, String content, String url) {
        this.author = author;
        this.content = content;
        this.url = url;
    }

    public String getAuthor() {
        return author;
    }

    public ReviewModel setAuthor(String author) {
        this.author = author;
        return this;
    }

    public String getContent() {
        return content;
    }

    public ReviewModel setContent(String content) {
        this.content = content;
        return this;
    }

    public String getUrl() {
        return url;
    }

    public ReviewModel setUrl(String url) {
        this.url = url;
        return this;
    }
}
