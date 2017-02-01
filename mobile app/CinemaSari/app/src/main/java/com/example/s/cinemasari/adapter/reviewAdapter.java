package com.example.s.cinemasari.adapter;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import com.example.s.cinemasari.R;
import com.example.s.cinemasari.model.ReviewModel;
import com.example.s.cinemasari.model.TrailerModel;

import java.util.List;

/**
 * Created by S on 5/10/2016.
 */
public class reviewAdapter extends ArrayAdapter<ReviewModel> {


    public reviewAdapter(Context context, List<ReviewModel> objects) {
        super(context, 0, objects);
    }
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        ReviewModel review=getItem(position);
        if(convertView==null){
            convertView= LayoutInflater.from(getContext()).inflate(R.layout.list_review_view,parent,false);
        }
        TextView authourtxt= (TextView) convertView.findViewById(R.id.textauthor);
        authourtxt.setText(review.getAuthor());
        TextView contenttxt= (TextView) convertView.findViewById(R.id.textcontent);
        contenttxt.setText(review.getContent());
        TextView urltxt= (TextView) convertView.findViewById(R.id.texturl);
        urltxt.setText(review.getUrl());
        return convertView;
    }
}
