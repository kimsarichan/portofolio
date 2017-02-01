package com.example.s.cinemasari;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.TaskStackBuilder;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.AsyncTask;
import android.preference.PreferenceManager;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.support.v4.app.NotificationCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.GridView;

import com.example.s.cinemasari.adapter.movieAdapter;
import com.example.s.cinemasari.model.MovieModel;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

/**
 * A placeholder fragment containing a simple view.
 */
public class MainActivityFragment extends Fragment {
    private final String LOG_TAG = MainActivityFragment.class.getSimpleName();
    movieAdapter mMovieGridAdapter;
    private ArrayList<MovieModel> mMovieArrayList;
    public MainActivityFragment() {
        setHasOptionsMenu(true);
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (savedInstanceState == null) {

            mMovieArrayList = new ArrayList<>();
            mMovieGridAdapter = new movieAdapter(getActivity(), new ArrayList<MovieModel>());

        }

    }
    private void updateMovie(){
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getActivity());
        String SORT_BY = prefs.getString(getString(R.string.pref_sort_key),
                getString(R.string.pref_popular));
        if(SORT_BY!="") {
            FetchMovieData movieData = new FetchMovieData();
            movieData.execute(SORT_BY);
        }else{
            FetchMovieData movieData = new FetchMovieData();
            movieData.execute("popular");
        }
    }

    @Override
    public void onStart(){
        super.onStart();
        updateMovie();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_main, container, false);
        GridView gridView = (GridView) rootView.findViewById(R.id.gridview);
        gridView.setAdapter(mMovieGridAdapter);
        gridView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                MovieModel movieClick = mMovieGridAdapter.getItem(position);

                Intent intent = new Intent(getActivity(), DetailActivity.class)
                        .putExtra(Intent.EXTRA_TEXT, movieClick);
                startActivity(intent);
            }
        });

        return rootView;

    }
    public void notifytry(){
        NotificationManager notificationManager = (NotificationManager)this.getContext().getSystemService(this.getContext().NOTIFICATION_SERVICE);
        @SuppressWarnings("deprecation")
        MovieModel movieClick = mMovieGridAdapter.getItem(0);

        Intent notificationIntent = new Intent(getActivity(), DetailActivity.class)
                .putExtra(Intent.EXTRA_TEXT, movieClick);
        PendingIntent pendingIntent = PendingIntent.getActivity(getActivity(), 0,notificationIntent, 0);


        Notification.Builder builder = new Notification.Builder(this.getContext());

        builder.setAutoCancel(false);
        builder.setTicker("this is ticker text");
        builder.setContentTitle("Cinema Sari Notification");
        builder.setContentText("We recommend you to watch "+movieClick.getTittle());
        builder.setSmallIcon(R.mipmap.ic_launcher);
        builder.setContentIntent(pendingIntent);
        builder.setOngoing(true);
        builder.build();

        Notification myNotication = builder.getNotification();
        notificationManager.notify(11, myNotication);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if(id== R.id.action_refresh){
            updateMovie();
            notifytry();
            return  true;
        }

        return super.onOptionsItemSelected(item);
    }

    public class FetchMovieData extends AsyncTask<String,Void,MovieModel[]> {

        private final String LOG_TAG = FetchMovieData.class.getSimpleName();

        /* The date/time conversion code is going to be moved outside the asynctask later,
        * so for convenience we're breaking it out into its own method now.
        */
        private String getReadableDateString(String date) {
            // Because the API returns date in YYYY-MM-DD,
            // it must be converted to readable date.
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
            SimpleDateFormat readableFormat = new SimpleDateFormat("MMMM dd, yyyy");
            try {
                Date mDate = dateFormat.parse(date);
                return readableFormat.format(mDate);
            } catch (ParseException e) {
                Log.e(LOG_TAG, "Error Date : " + e);
                e.printStackTrace();
            }
            return null;
        }

        /**
         * Take the Array Movie representing the complete movie data in JSON Format and
         * pull out the data we need to construct the Movies needed for the wireframes.
         * <p/>
         * Fortunately parsing is easy:  constructor takes the JSON string and converts it
         * into an Object hierarchy for us.
         */
        private MovieModel[] getMovieDataFromJson(String movieJsonStr) throws JSONException {

            // These are the names of the JSON objects that need to be extracted.
            final String MOVIE_ID = "id";
            final String MOVIE_LIST = "results";
            final String MOVIE_POSTER = "poster_path";
            final String MOVIE_ORI_TITLE = "original_title";
            final String MOVIE_SYNOPSIS = "overview";
            final String MOVIE_RATING = "vote_average";
            final String MOVIE_RELEASE = "release_date";

            JSONObject movieJson = new JSONObject(movieJsonStr);
            JSONArray movieArray = movieJson.getJSONArray(MOVIE_LIST);

            MovieModel [] mMovie = new MovieModel[movieArray.length()];
            for (int i = 0; i < movieArray.length(); i++) {
                int id;
                String poster_path;
                String title;
                String synopsis;
                String rating;
                String release;

                String urlPoster = "http://image.tmdb.org/t/p/w185/";

                JSONObject movieObj = movieArray.getJSONObject(i);
                id = movieObj.getInt(MOVIE_ID);
                poster_path = movieObj.getString(MOVIE_POSTER);
                title = movieObj.getString(MOVIE_ORI_TITLE);
                synopsis = movieObj.getString(MOVIE_SYNOPSIS);
                rating = String.valueOf(movieObj.getDouble(MOVIE_RATING));
                release = movieObj.getString(MOVIE_RELEASE);


                mMovie[i] = new MovieModel(id, urlPoster.concat(poster_path), title, synopsis, rating, release);
            }

            return mMovie;
        }

        @Override
        protected MovieModel[] doInBackground(String... params) {

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

                final String MOVIEDB_BASE_URL = "http://api.themoviedb.org/3/movie/"+params[0];
                final String API_KEY_PARAM = "api_key";

                Uri builtUri = Uri.parse(MOVIEDB_BASE_URL).buildUpon()
                        .appendQueryParameter(API_KEY_PARAM, BuildConfig.MOVIE_API)
                        .build();

                URL url = new URL(builtUri.toString());

                Log.v(LOG_TAG, "URL : " + url);

                // Create the request to OpenWeatherMap, and open the connection
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
        protected void onPostExecute(MovieModel[] movieResults) {
            if (movieResults != null) {
                mMovieGridAdapter.clear();
                for (MovieModel m : movieResults) {
                    mMovieGridAdapter.add(m);
                }
                mMovieArrayList.clear();
                mMovieArrayList.addAll(Arrays.asList(movieResults));
            }
        }

    }


}
