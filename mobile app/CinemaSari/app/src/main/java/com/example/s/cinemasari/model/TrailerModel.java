package com.example.s.cinemasari.model;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by S on 5/9/2016.
 */
public class TrailerModel implements Parcelable {

    String key;
    String name;

    public TrailerModel(String key, String name) {
        this.key = key;
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public String getKey() {
        return key;
    }

    protected TrailerModel(Parcel in) {
        key = in.readString();
        name = in.readString();
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(key);
        dest.writeString(name);
    }

    public static final Parcelable.Creator<TrailerModel> CREATOR = new Parcelable.Creator<TrailerModel>() {

        @Override
        public TrailerModel createFromParcel(Parcel in) {
            return new TrailerModel(in);
        }

        @Override
        public TrailerModel[] newArray(int size) {
            return new TrailerModel[size];
        }
    };
}
