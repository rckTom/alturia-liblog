#pragma once

#include <vector>
#include <map>
#include <string>
#include <cstdint>

class Alturialog {
	std::map<int, Track> tracks;
public:
	Alturialog(std::string path);
};

class Track {
	std::string format;
	int entry_length;
	std::vector<std::byte> data;
};
