function jac(movieid1,movieid2)
% Path and file names
pathname = 'data/';
ratingsfname = 'u.data';
itemsfname = 'u.item';

% Read in the items
fid = fopen([pathname itemsfname]);
items = {};
items{1682} = '';
%movie 1 
i=movieid1
items{i} = fgetl(fid);
pos = strfind(items{i},'|');
%movie2
j=movieid2
items{j} = fgetl(fid);
pos2 = strfind(items{i},'|');
l=0
m=0
n=0
for(k=5:22),
 
  %if (items{i}(pos(k)) != ('|'))
    if(items{i}(pos(k)+1)=='1' && items{j}(pos(k)+1)=='1' )
      l=l+1
    elseif(items{i}(pos(k)+1)=='0' && items{j}(pos(k)+1)=='1' )
      m=m+1
    elseif(items{i}(pos(k)+1)=='1' && items{j}(pos(k)+1)=='0' )
      n=n+1
    end
  %end
end
jac = l/(m+n+l)



items{j} = items{j}((pos(3)+1):(pos(23)-1));
fprintf(items{j})

fclose(fid);