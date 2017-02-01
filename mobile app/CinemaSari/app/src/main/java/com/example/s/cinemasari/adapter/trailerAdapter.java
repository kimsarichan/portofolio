package com.example.s.cinemasari.adapter;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import com.example.s.cinemasari.R;

import com.example.s.cinemasari.model.TrailerModel;

import java.util.List;

/**
 * Created by S on 5/9/2016.
 */
public class trailerAdapter extends ArrayAdapter<TrailerModel> {
    public trailerAdapter(Context context,List<TrailerModel> trailerList){
        super(context,0,trailerList);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        TrailerModel trailer=getItem(position);
        if(convertView==null){
            convertView= LayoutInflater.from(getContext()).inflate(R.layout.list_trailer_view,parent,false);
        }
        TextView trailertxt= (TextView) convertView.findViewById(R.id.trailerTitle);
        Log.v("trailer",trailer.getName());
        trailertxt.setText(trailer.getName());
        return convertView;
    }
}
