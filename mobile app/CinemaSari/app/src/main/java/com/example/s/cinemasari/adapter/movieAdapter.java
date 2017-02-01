package com.example.s.cinemasari.adapter;

import android.content.Context;
import android.graphics.Movie;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;


import com.example.s.cinemasari.R;
import com.example.s.cinemasari.model.MovieModel;
import com.squareup.picasso.Picasso;

import java.util.List;

/**
 * Created by S on 5/7/2016.
 */
public class movieAdapter extends ArrayAdapter<MovieModel>{
    public movieAdapter(Context context,List<MovieModel> movieList){
        super(context,0,movieList);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        MovieModel movie=getItem(position);
        if(convertView==null){
            convertView= LayoutInflater.from(getContext()).inflate(R.layout.list_image_view,parent,false);

        }
        ImageView miniView=(ImageView)convertView.findViewById(R.id.miniView);
        Picasso.with(getContext()).load(movie.getPoster()).into(miniView);
        return convertView;
    }
}
