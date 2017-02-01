function sortdata()
pathname = 'data/';
ratingsfname = 'u.data';
ratings = load([pathname ratingsfname]);
%selectedrows = find(ratings(:,1) == uid);
ys = ratings(1,:);
fprintf(ys(i,2))
end