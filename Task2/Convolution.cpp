#include <iostream>
#include <vector>
#include <random>
#include <algorithm> //for sort function
using namespace std;

class Point{
private:
    int x;
    int y;

public:
	Point()
	{
		x = 0;
		y = 0;
	}
    Point(int x0, int y0)
    {
        x = x0;
        y = y0;
    }
    int GetX()
    {
        return x;
    }
    int GetY()
    {
        return y;
    }
    void Set(int x0, int y0)
    {
        x = x0;
        y = y0;
    }
};

void ShowMat(vector<vector<int>> Mat)
{
	int y = Mat.size();
	int x = Mat[0].size();

	for (int i = 0; i < y; ++i)
	{
		for (int j = 0; j < x; ++j)
		{
			cout.width(5);
			cout << Mat[i][j];
		}
		cout << endl;
	}
}

void ZeroPadded(vector<vector<int>>& src, Point& kernal_size, vector<vector<int>>& src_padded)
{
     //get src_size
    int src_size_w = src[0].size();
    int src_size_h = src.size();

	//get src_size
	int kernal_w = kernal_size.GetX();
	int kernal_h = kernal_size.GetY();

	//get src_padded_size
	int src_padded_size_w = src_size_w + kernal_w - 1;
	int src_padded_size_h = src_size_h + kernal_h - 1;

    vector<int> row(src_padded_size_w, 0);
    vector<vector<int>> temp(src_padded_size_h, row);
    for(int i = 0; i < src_size_h; ++i)
    {
        for(int j = 0; j < src_size_w; ++j)
        {
            temp[kernal_h /2 + i][kernal_w /2 + j] = src[i][j];
        }
    }
	src_padded = temp;
	cout << endl << endl;
	ShowMat(src_padded);
}


void ReplicaPadded(vector<vector<int>>& src, Point& kernal_size, vector<vector<int>>& src_padded)
{
	//get src_size
	int src_size_w = src[0].size();
	int src_size_h = src.size();

	//get src_size
	int kernal_w = kernal_size.GetX();
	int kernal_h = kernal_size.GetY();

	//get src_padded_size
	int src_padded_size_w = src_size_w + kernal_w - 1;
	int src_padded_size_h = src_size_h + kernal_h - 1;
	
	int pad_size_h = kernal_h / 2;
	int pad_size_w = kernal_w / 2;
	vector<vector<int>> temp(src);

	//padding in height
	for (int i = 0; i < pad_size_h; ++i)
	{
		temp.insert(temp.begin(), src[0]);
		temp.push_back(src[src_size_h - 1]);
	}

	//padding in width
	for (int i = 0; i < src_padded_size_h; ++i)
	{
		for (int j = 0; j < pad_size_w; ++j)
		{
			temp[i].insert(temp[i].begin(), temp[i][0]);
			temp[i].push_back(temp[i][temp[i].size() - 1]);
		}
	}
	src_padded = temp;
}

void GetROI(vector<vector<int>>& src, Point& start, Point& end, vector<int>& result)
{
    result.clear();
    for(int i = start.GetX(); i < end.GetX() + 1; ++i)
    {
        for(int j = start.GetY(); j < end.GetY() + 1; ++j )
        {
            result.push_back(src[i][j]);
        }
    }
}

void medianBlur(vector<vector<int>>& src, vector<vector<int>> kernel, string padding_way)
{
    //igonor input para invalid check

    vector<vector<int>> src_padded;
    vector<vector<int>> dst = src;

    //get kernal_size
    Point kernal_size(kernel.size(), kernel[0].size());
    int kernal_w = kernal_size.GetX();
    int kernal_h = kernal_size.GetY();

    //get padded image
    if(padding_way == "REPLICA")
    {
        ReplicaPadded(src, kernal_size, src_padded);
    }
	else //"ZERO"
	{

	}
    {
        ZeroPadded(src, kernal_size, src_padded);
    }

    //get src_padded_size
    Point src_padded_size(src_padded.size(), src_padded[0].size());
    int src_padded_size_w = src_padded_size.GetX();
    int src_padded_size_h = src_padded_size.GetY();

    
    Point start, end, center;
    int center_value = 0;
    vector<int> ROI;
    for(int i = 0; i < src_padded_size_h - kernal_h + 1; ++i)
    {
        for(int j = 0; j < src_padded_size_w - kernal_w + 1; ++j)
        {
            start.Set(i, j);
            end.Set(i+ kernal_h - 1, j+ kernal_w - 1);
            center.Set(i + kernal_h/2, j + kernal_w / 2);
            GetROI(src_padded, start, end, ROI);
			sort(ROI.begin(), ROI.end());
            int middle = ROI.size()/2;
            center_value = ROI[middle];
            dst[i][j] = center_value;
        }
    }
	src = dst;
}


int main()
{
	//source size
	const int src_col = 10;
	const int src_row = 10;

	//kernal size
	const int kernal_col = 3;
	const int kernal_row = 3;

	default_random_engine e;
	uniform_int_distribution<unsigned> u(0, 9);
	vector<vector<int>> src;
	vector<vector<int>> kernal;
	vector<vector<int>> src_padded;
	vector<int> row_value;
	//generate src
	for(int i = 0; i < src_row; ++i)
	{ 
		row_value.clear();
		for (int j = 0; j < src_col; ++j)
		{
			row_value.push_back(u(e));
		}
		src.push_back(row_value);
	}

	//generate kernal
	for (int i = 0; i < kernal_row; ++i)
	{
		row_value.clear();
		for (int j = 0; j < kernal_col; ++j)
		{
			row_value.push_back(1);
		}
		kernal.push_back(row_value);
	}
	
	ShowMat(src);
	cout << endl << endl;
	ShowMat(kernal);

	Point kernal_size(kernal_row, kernal_col);

	////ZeroPadded(src, kernal_size, src_padded);
	//ReplicaPadded(src, kernal_size, src_padded);
	//cout << endl << endl;
	//ShowMat(src_padded);

	medianBlur(src, kernal, "ZERO");

	cout << endl << endl;
	ShowMat(src);
	return 0;
}