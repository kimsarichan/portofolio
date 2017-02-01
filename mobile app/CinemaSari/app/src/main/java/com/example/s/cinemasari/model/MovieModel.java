package com.example.s.cinemasari.model;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by S on 5/7/2016.
 */
public class MovieModel implements Parcelable {
    int id;
    String poster;
    String tittle;
    String synopsis;
    String rating;
    String release;

    public MovieModel(int id, String poster, String tittle, String synopsis, String rating, String release) {
        this.id = id;
        this.poster = poster;
        this.tittle = tittle;
        this.synopsis = synopsis;
        this.rating = rating;
        this.release = release;
    }

    public int getId() {
        return id;
    }

    public String getPoster() {
        return poster;
    }

    public String getTittle() {
        return tittle;
    }

    public String getSynopsis() {
        return synopsis;
    }

    public String getRating() {
        return rating;
    }

    public String getRelease() {
        return release;
    }

    protected MovieModel(Parcel in) {
        id = in.readInt();
        poster = in.readString();
        tittle = in.readString();
        synopsis = in.readString();
        rating = in.readString();
        release = in.readString();
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(id);
        dest.writeString(poster);
        dest.writeString(tittle);
        dest.writeString(synopsis);
        dest.writeString(rating);
        dest.writeString(release);
    }

    @SuppressWarnings("unused")
    public static final Parcelable.Creator<MovieModel> CREATOR = new Parcelable.Creator<MovieModel>() {
        @Override
        public MovieModel createFromParcel(Parcel in) {
            return new MovieModel(in);
        }

        @Override
        public MovieModel[] newArray(int size) {
            return new MovieModel[size];
        }
    };
}
