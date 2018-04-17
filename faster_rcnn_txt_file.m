%%
load('resized_dark_shore_f_rcnn.mat')

%%



%%



for i = 1:25
    dlmwrite(strcat("resized_dark_shore_scores_",string(find_true(i)),".txt"),im_processed{i,1}.scores);
    dlmwrite(strcat("resized_dark_shore_boxes_",string(find_true(i)),".txt"),im_processed{i,1}.boxes);
end

% for i = 26:50
%     dlmwrite(strcat("dark_shore_scores_",string(find_true(i-25)),".txt"),im_processed{i,1}.scores);
%     dlmwrite(strcat("dark_shore_boxes_",string(find_true(i-25)),".txt"),im_processed{i,1}.boxes);
% end
% 
% for i = 51:75
%     dlmwrite(strcat("light_sea_scores_",string(find_true(i-50)),".txt"),im_processed{i,1}.scores);
%     dlmwrite(strcat("light_sea_boxes_",string(find_true(i-50)),".txt"),im_processed{i,1}.boxes);
% end
% 
% for i = 76:100
%     dlmwrite(strcat("light_shore_scores_",string(find_true(i-75)),".txt"),im_processed{i,1}.scores);
%     dlmwrite(strcat("light_shore_boxes_",string(find_true(i-75)),".txt"),im_processed{i,1}.boxes);
% end
    
%     
%     
%     
% %     images = []
% %     images(end+1) 
%     boxes = [];
%     % scores = [];
%     for j = 1:300
%         im_processed{i,1}.scores(j);
%         imshow(im_processed{76,1}.img)
%         if im_processed{i,1}.scores(j) >= 0.25
%             mat2str(im_processed{i,1}.boxes(j,:))
%             % boxes(end+1) = int2str(2)
%             a = mat2str(im_processed{i,1}.boxes(j,:))
%             boxes(end+1) = a;
%             % scores = append(scores, im_processed{i,1}.scores(j));
%         end
%     % WRITE TO FILE
%     fid = fopen('test.txt','w');
%     text = [num2str(i)];
%     for k = 1:length(boxes)
%         text(end+1) = ';'
%         text(end+1) = boxes(k)
%     end
%     text
%     fprintf(fid, text);
%     end
% end
% 
% fclose(fid);

function true_image_num = find_true(i)
    if i == 1
        true_image_num = 1
    elseif i == 12
        true_image_num = 2
    elseif i >= 19 && i <= 25
        true_image_num = i - 16
    elseif i >= 2 && i <= 11
        true_image_num = i+8
    elseif i >= 13 && i <= 18
        true_image_num = i + 7
    end
        
end