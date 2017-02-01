package com.example.s.cinemasari;

import android.content.ActivityNotFoundException;
import android.content.Intent;

import android.net.Uri;
import android.os.AsyncTask;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ImageView;
import android.support.v7.widget.ShareActionProvider;
import android.widget.ListView;
import android.widget.TextView;
import android.support.v4.view.MenuItemCompat;

import com.example.s.cinemasari.adapter.reviewAdapter;
import com.example.s.cinemasari.adapter.trailerAdapter;
import com.example.s.cinemasari.model.MovieModel;
import com.example.s.cinemasari.model.ReviewModel;
import com.example.s.cinemasari.model.TrailerModel;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

/**
 * A placeholder fragment containing a simple view.
 */
public class DetailActivityFragment extends Fragment {
    MovieModel movie;
    private  String movieTitle;
    private trailerAdapter mTrailerAdapter;
    private ArrayList<TrailerModel> mTrailerList;
    private reviewAdapter mReviewAdapter;
    private ArrayList<ReviewModel> mReviewList;
    private ShareActionProvider mShareActionProvider;
    private final String LOG_TAG = DetailActivityFragment.class.getSimpleName();
    public DetailActivityFragment() {
        setHasOptionsMenu(true);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        Intent intent = getActivity().getIntent();

        View rootView = inflater.inflate(R.layout.fragment_detail, container, false);


        if (intent != null && intent.hasExtra(Intent.EXTRA_TEXT)) {
            movie = intent.getParcelableExtra(Intent.EXTRA_TEXT);

            ImageView poster = (ImageView) rootView.findViewById(R.id.poster_thumb);
            Picasso.with(getContext()).load(movie.getPoster()).into(poster);

            ((TextView) rootView.findViewById(R.id.textTitle)).setText(movie.getTittle());
            ((TextView) rootView.findViewById(R.id.textRating)).setText(movie.getRating());
            ((TextView) rootView.findViewById(R.id.textRelease)).setText(movie.getRelease());
            ((TextView) rootView.findViewById(R.id.textSynopsis)).setText(movie.getSynopsis());
            movieTitle= movie.getTittle();
            mTrailerList = new ArrayList<>();
            mTrailerAdapter = new trailerAdapter(getActivity(), mTrailerList);
            mReviewList= new ArrayList<>();
            mReviewAdapter = new reviewAdapter(getActivity(), mReviewList);
            ListView lvReview=(ListView) rootView.findViewById(R.id.listReview);
            lvReview.setAdapter(mReviewAdapter);
           ListView lvTrailer = (ListView) rootView.findViewById(R.id.listTrailer);
            lvTrailer.setAdapter(mTrailerAdapter);

            // Youtube Intent
            lvTrailer.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    String videoID = mTrailerAdapter.getItem(position).getKey();
                    try {
                        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("vnd.youtube:" + videoID));
                        startActivity(intent);
                    } catch (ActivityNotFoundException ex) {
                        Intent intent = new Intent(Intent.ACTION_VIEW,
                                Uri.parse("http://www.youtube.com/watch?v=" + videoID));
                        startActivity(intent);
                    }
                }
            });
            lvReview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    String review_url=mReviewAdapter.getItem(position).getUrl();
                    Intent intent = new Intent(Intent.ACTION_VIEW,
                            Uri.parse(review_url));
                    startActivity(intent);
                }
            });
            getReview(movie.getId());

            getTrailer(movie.getId());
        }
        return  rootView;
    }
    protected void getTrailer(int idFilm) {
        FetchTrailer trailerTask = new FetchTrailer();
        trailerTask.execute(idFilm);
        Log.i(LOG_TAG, "Get trailer");
    }
    protected void getReview(int idFilm) {
        FetchReview trailerTask = new FetchReview();
        trailerTask.execute(idFilm);
        Log.i(LOG_TAG, "Get review");
    }
    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        // Inflate the menu; this adds items to the action bar if it is present.
        inflater.inflate(R.menu.menu_detail, menu);

        // Retrieve the share menu item
        MenuItem menuItem = menu.findItem(R.id.action_share);

        // Get the provider and hold onto it to set/change the share intent.
        mShareActionProvider = (ShareActionProvider) MenuItemCompat.getActionProvider(menuItem);

        // If onLoadFinished happens before this, we can go ahead and set the share intent now.
        if (movieTitle != null) {
            mShareActionProvider.setShareIntent(createShareMovieIntent());
        }
    }

    private Intent createShareMovieIntent() {
        Intent shareIntent = new Intent(Intent.ACTION_SEND);
        shareIntent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_WHEN_TASK_RESET);
        shareIntent.setType("text/plain");
        shareIntent.putExtra(Intent.EXTRA_TEXT,"Lets Watch "+ movieTitle );
        return shareIntent;
    }

    public  class FetchTrailer extends AsyncTask<Integer,Void,TrailerModel[]> {

        private final String LOG_TAG = FetchTrailer.class.getSimpleName();

        /**
         * Take the Array Movie representing the complete movie data in JSON Format and
         * pull out the data we need to construct the Movies needed for the wireframes.
         * <p/>
         * Fortunately parsing is easy:  constructor takes the JSON string and converts it
         * into an Object hierarchy for us.
         */
        private TrailerModel[] getMovieDataFromJson(String movieJsonStr) throws JSONException {

            // These are the names of the JSON objects that need to be extracted.
            final String TRAILER_LIST = "results";
            final String TRAILER_KEY_URL = "key";
            final String TRAILER_NAME = "name";

            JSONObject trailerJson = new JSONObject(movieJsonStr);
            JSONArray trailerArray = trailerJson.getJSONArray(TRAILER_LIST);

            TrailerModel trailerItem[] = new TrailerModel[trailerArray.length()];
            for (int i = 0; i < trailerArray.length(); i++) {

                String key;
                String name;

                JSONObject trailerObj = trailerArray.getJSONObject(i);
                key = trailerObj.getString(TRAILER_KEY_URL);
                name = trailerObj.getString(TRAILER_NAME);

                trailerItem[i] = new TrailerModel(key, name);
            }

            return trailerItem;
        }

        @Override
        protected TrailerModel[] doInBackground(Integer... params) {

            // These two need to be declared outside the try/catch
            // so that they can be closed in the finally block.
            HttpURLConnection urlConnection = null;
            BufferedReader reader = null;

            // Will contain the raw JSON response as a string.
            String movieJsonStr = null;

            try {
                // Construct the URL for the The Movie DB query
                // Possible parameters are available at The Movie DB's apiary page, at
                // http://docs.themoviedb.apiary.io/#

                final String MOVIEDB_TRAILER = "http://api.themoviedb.org/3/movie/";
                final String API_KEY_PARAM = "api_key";

                final String MOVIE_ID = params[0].toString();
                final String VIDEO_PARAM = "videos";

                Uri builtUri = Uri.parse(MOVIEDB_TRAILER).buildUpon()
                        .appendPath(MOVIE_ID)
                        .appendPath(VIDEO_PARAM)
                        .appendQueryParameter(API_KEY_PARAM, BuildConfig.MOVIE_API)
                        .build();

                URL url = new URL(builtUri.toString());
                Log.v(LOG_TAG, "URl TRailer"+url);
                // Create the request to MovieDB, and open the connection
                urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("GET");
                urlConnection.connect();

                // Read the input stream into a String
                InputStream inputStream = urlConnection.getInputStream();
//                StringBuffer buffer = new StringBuffer();
                StringBuilder buffer = new StringBuilder();
                if (inputStream == null) {
                    // Nothing to do.
                    return null;
                }
                reader = new BufferedReader(new InputStreamReader(inputStream));

                String line;
                while ((line = reader.readLine()) != null) {
                    // Since it's JSON, adding a newline isn't necessary (it won't affect parsing)
                    // But it does make debugging a *lot* easier if you print out the completed
                    // buffer for debugging.
//                    buffer.append(line + "\n");
                    buffer.append(line);
                }

                if (buffer.length() == 0) {
                    // Stream was empty.  No point in parsing.
                    return null;
                }

                movieJsonStr = buffer.toString();

            } catch (IOException e) {
                Log.e(LOG_TAG, "Error ", e);
                // If the code didn't successfully get the weather data, there's no point in attemping
                // to parse it.
                return null;
            } finally {
                if (urlConnection != null) {
                    urlConnection.disconnect();
                }
                if (reader != null) {
                    try {
                        reader.close();
                    } catch (final IOException e) {
                        Log.e(LOG_TAG, "Error closing stream", e);
                    }
                }
            }

            try {
                return getMovieDataFromJson(movieJsonStr);
            } catch (JSONException e) {
                Log.e(LOG_TAG, e.getMessage(), e);
                e.printStackTrace();
            }

            // This will only happen if there was an error getting or parsing the forecast.
            return null;
        }

        @Override
        protected void onPostExecute(TrailerModel[] trailerResults) {
            if (trailerResults != null) {
                mTrailerAdapter.clear();
                for (TrailerModel m : trailerResults) {
                    mTrailerAdapter.add(m);
                }
                mTrailerList.clear();
                mTrailerList.addAll(Arrays.asList(trailerResults));
            }
        }
    }
    public  class FetchReview  extends AsyncTask<Integer,Void,ReviewModel[]> {
        private ReviewModel[] getMovieDataFromJson(String movieJsonStr) throws JSONException {

            // These are the names of the JSON objects that need to be extracted.
            final String REVIEW_LIST = "results";
            final String REVIEW_AUTHOR = "author";
            final String REVIEW_CONTENT = "content";
            final String REVIEW_URL = "url";

            JSONObject reviewJson = new JSONObject(movieJsonStr);
            JSONArray reviewArray = reviewJson.getJSONArray(REVIEW_LIST);

            ReviewModel reviewItem[] = new ReviewModel[reviewArray.length()];
            for (int i = 0; i < reviewArray.length(); i++) {

                String author;
                String content;
                String url;

                JSONObject review = reviewArray.getJSONObject(i);
                author = review.getString(REVIEW_AUTHOR);
                content = review.getString(REVIEW_CONTENT);
                url = review.getString(REVIEW_URL);
                reviewItem[i] = new ReviewModel(author,content,url);
            }

            return reviewItem;
        }


        @Override
        protected ReviewModel[] doInBackground(Integer... params) {
            // These two need to be declared outside the try/catch
            // so that they can be closed in the finally block.
            HttpURLConnection urlConnection = null;
            BufferedReader reader = null;

            // Will contain the raw JSON response as a string.
            String movieJsonStr = null;

            try {
                // Construct the URL for the The Movie DB query
                // Possible parameters are available at The Movie DB's apiary page, at
                // http://docs.themoviedb.apiary.io/#

                final String MOVIEDB_REVIEW = "http://api.themoviedb.org/3/movie/";
                final String API_KEY_PARAM = "api_key";

                final String MOVIE_ID = params[0].toString();
                final String VIDEO_PARAM = "reviews";

                Uri builtUri = Uri.parse(MOVIEDB_REVIEW).buildUpon()
                        .appendPath(MOVIE_ID)
                        .appendPath(VIDEO_PARAM)
                        .appendQueryParameter(API_KEY_PARAM, BuildConfig.MOVIE_API)
                        .build();

                URL url = new URL(builtUri.toString());
                Log.v(LOG_TAG, "URl Review"+url);
                // Create the request to MovieDB, and open the connection
                urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("GET");
                urlConnection.connect();

                // Read the input stream into a String
                InputStream inputStream = urlConnection.getInputStream();
//                StringBuffer buffer = new StringBuffer();
                StringBuilder buffer = new StringBuilder();
                if (inputStream == null) {
                    // Nothing to do.
                    return null;
                }
                reader = new BufferedReader(new InputStreamReader(inputStream));

                String line;
                while ((line = reader.readLine()) != null) {
                    // Since it's JSON, adding a newline isn't necessary (it won't affect parsing)
                    // But it does make debugging a *lot* easier if you print out the completed
                    // buffer for debugging.
//                    buffer.append(line + "\n");
                    buffer.append(line);
                }

                if (buffer.length() == 0) {
                    // Stream was empty.  No point in parsing.
                    return null;
                }

                movieJsonStr = buffer.toString();

            } catch (IOException e) {
                Log.e(LOG_TAG, "Error ", e);
                // If the code didn't successfully get the weather data, there's no point in attemping
                // to parse it.
                return null;
            } finally {
                if (urlConnection != null) {
                    urlConnection.disconnect();
                }
                if (reader != null) {
                    try {
                        reader.close();
                    } catch (final IOException e) {
                        Log.e(LOG_TAG, "Error closing stream", e);
                    }
                }
            }

            try {
                return getMovieDataFromJson(movieJsonStr);
            } catch (JSONException e) {
                Log.e(LOG_TAG, e.getMessage(), e);
                e.printStackTrace();
            }

            // This will only happen if there was an error getting or parsing the forecast.
            return null;
        }
        @Override
        protected void onPostExecute(ReviewModel[] reviewResults) {
            if (reviewResults != null) {
                mReviewAdapter.clear();
                for (ReviewModel m : reviewResults) {
                    mReviewAdapter.add(m);
                }
                mReviewList.clear();
                mReviewList.addAll(Arrays.asList(reviewResults));
            }
        }
    }

}
